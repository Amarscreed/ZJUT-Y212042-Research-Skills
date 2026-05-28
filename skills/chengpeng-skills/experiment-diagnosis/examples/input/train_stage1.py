#!/usr/bin/env python3
"""
Stage 1: Pre-train Agent A (Vision Analyst) + Agent B (Draft Writer)
====================================================================

Training pipeline:
1. Agent A: ViT-L/14 → VFP (3-level) → MLP (768→256→14) for CheXpert 14-class
2. Agent B: Q-Former (32 queries) → DASTs → DMSR → Vicuna-7B + LoRA (r=16, alpha=32)
3. Loss: L_ce + 0.5 * L_vlp (CXR-CLIP contrastive)
4. lr=5e-5, bs=16, AdamW

Usage:
    python train_stage1.py --config configs/stage1.yaml
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from experiments.models.agent_a_vision import AgentA_VisionAnalyst
from experiments.models.agent_b_draft import AgentB_DraftWriter
from experiments.utils.losses import Stage1Loss

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("train_stage1")


def load_config(config_path: str) -> dict:
    """Load YAML config file.

    TODO: Replace with proper hydra/omegaconf loading.
    """
    import yaml
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    logger.info(f"Loaded config from {config_path}")
    return config


def build_models(config: dict, device: torch.device) -> tuple[nn.Module, nn.Module]:
    """Build Agent A and Agent B from config.

    TODO: Implement proper model loading from pretrained checkpoints.
    """
    a_cfg = config["model"]["agent_a"]
    b_cfg = config["model"]["agent_b"]

    # Agent A: Vision Analyst
    agent_a = AgentA_VisionAnalyst(
        vit_embed_dim=a_cfg["vit_embed_dim"],
        mlp_hidden_dim=a_cfg["mlp"]["hidden_dim"],
        num_classes=a_cfg["mlp"]["out_dim"],
        vfp_levels=a_cfg["visual_feature_pyramid"]["levels"],
        vfp_out_dim=a_cfg["visual_feature_pyramid"]["out_channels"],
    ).to(device)

    # Load ViT backbone (placeholder)
    agent_a.load_vit_backbone(a_cfg.get("checkpoint"))

    # Agent B: Draft Writer
    b_qf = b_cfg["qformer"]
    b_dast = b_cfg["dast"]
    b_dmsr = b_cfg["dmsr"]
    b_lora = b_cfg["lora"]

    agent_b = AgentB_DraftWriter(
        qformer_num_queries=b_qf["num_queries"],
        qformer_hidden_dim=b_qf["hidden_dim"],
        qformer_num_heads=b_qf["num_heads"],
        qformer_num_layers=b_qf["num_layers"],
        dast_num_tokens=b_dast["num_tokens"],
        dast_num_blocks=b_dast["num_blocks"],
        dast_hidden_dim=b_qf["hidden_dim"],
        dmsr_num_clusters=b_dmsr["num_clusters"],
        dmsr_top_k=b_dmsr["top_k"],
        lora_r=b_lora["r"],
        lora_alpha=b_lora["alpha"],
        lora_target_modules=b_lora["target_modules"],
    ).to(device)

    # Load Vicuna-7B backbone (placeholder)
    agent_b.load_vicuna_backbone(b_cfg.get("checkpoint"))

    logger.info(f"Agent A parameters: {sum(p.numel() for p in agent_a.parameters()):,}")
    logger.info(f"Agent B parameters: {sum(p.numel() for p in agent_b.parameters()):,}")

    return agent_a, agent_b


def build_optimizer(
    agent_a: nn.Module,
    agent_b: nn.Module,
    config: dict,
) -> torch.optim.Optimizer:
    """Build AdamW optimizer for both agents."""
    t_cfg = config["training"]
    param_groups = [
        {"params": agent_a.parameters(), "lr": t_cfg["learning_rate"]},
        {"params": agent_b.parameters(), "lr": t_cfg["learning_rate"]},
    ]
    optimizer = torch.optim.AdamW(
        param_groups,
        lr=t_cfg["learning_rate"],
        weight_decay=t_cfg["weight_decay"],
        eps=t_cfg["adam_epsilon"],
    )
    return optimizer


def build_dataloaders(config: dict) -> tuple[DataLoader, DataLoader]:
    """Build placeholder train/val dataloaders.

    TODO: Implement actual MIMIC-CXR dataset loading.
    """
    class PlaceholderCXRDataset(torch.utils.data.Dataset):
        """Placeholder dataset for testing the training loop."""

        def __init__(self, num_samples: int, image_size: int, num_classes: int):
            self.num_samples = num_samples
            self.image_size = image_size
            self.num_classes = num_classes

        def __len__(self):
            return self.num_samples

        def __getitem__(self, idx):
            return {
                "pixel_values": torch.randn(3, self.image_size, self.image_size),
                "labels": torch.randint(0, 2, (self.num_classes,)).float(),
                "input_ids": torch.randint(0, 100, (128,)),
                "attention_mask": torch.ones(128, dtype=torch.long),
                "text_features": torch.randn(256),
            }

    d_cfg = config["data"]
    t_cfg = config["training"]

    train_dataset = PlaceholderCXRDataset(
        num_samples=1000,
        image_size=d_cfg["image_size"],
        num_classes=len(d_cfg["chexpert_labels"]),
    )
    val_dataset = PlaceholderCXRDataset(
        num_samples=100,
        image_size=d_cfg["image_size"],
        num_classes=len(d_cfg["chexpert_labels"]),
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=t_cfg["batch_size"],
        shuffle=True,
        num_workers=d_cfg["num_workers"],
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=t_cfg["batch_size"],
        shuffle=False,
        num_workers=2,
        pin_memory=True,
    )

    logger.info(f"Train samples: {len(train_dataset)}, Val samples: {len(val_dataset)}")
    return train_loader, val_loader


def train_epoch(
    agent_a: nn.Module,
    agent_b: nn.Module,
    loss_fn: Stage1Loss,
    optimizer: torch.optim.Optimizer,
    loader: DataLoader,
    device: torch.device,
    epoch: int,
    writer: SummaryWriter,
    log_interval: int,
    gradient_accumulation_steps: int,
    max_grad_norm: float,
) -> float:
    """Run one training epoch."""
    agent_a.train()
    agent_b.train()

    total_loss = 0.0
    total_ce = 0.0
    total_vlp = 0.0
    num_batches = len(loader)

    for batch_idx, batch in enumerate(loader):
        pixel_values = batch["pixel_values"].to(device)
        labels = batch["labels"].to(device)
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        text_features = batch["text_features"].to(device)

        # Agent A forward
        a_output = agent_a(pixel_values)

        # Agent B forward (using Agent A's visual features)
        b_output = agent_b(
            pixel_values=None,
            visual_features=a_output.visual_features,
            input_ids=input_ids,
            attention_mask=attention_mask,
        )

        # Loss
        loss_output = loss_fn(
            logits=a_output.logits,
            labels=labels,
            visual_features=a_output.visual_features,
            text_features=text_features,
        )

        loss = loss_output.total / gradient_accumulation_steps
        loss.backward()

        total_loss += loss_output.total.item()
        total_ce += loss_output.ce_loss.item()
        total_vlp += loss_output.vlp_loss.item()

        # Gradient accumulation
        if (batch_idx + 1) % gradient_accumulation_steps == 0:
            nn.utils.clip_grad_norm_(
                list(agent_a.parameters()) + list(agent_b.parameters()),
                max_grad_norm,
            )
            optimizer.step()
            optimizer.zero_grad()

        # Logging
        if batch_idx % log_interval == 0 and batch_idx > 0:
            step = epoch * num_batches + batch_idx
            writer.add_scalar("train/loss", loss_output.total.item(), step)
            writer.add_scalar("train/ce_loss", loss_output.ce_loss.item(), step)
            writer.add_scalar("train/vlp_loss", loss_output.vlp_loss.item(), step)

            logger.info(
                f"Epoch {epoch}, Batch {batch_idx}/{num_batches} | "
                f"Loss: {loss_output.total.item():.4f} | "
                f"CE: {loss_output.ce_loss.item():.4f} | "
                f"VLP: {loss_output.vlp_loss.item():.4f}"
            )

    avg_loss = total_loss / num_batches
    avg_ce = total_ce / num_batches
    avg_vlp = total_vlp / num_batches

    logger.info(
        f"Epoch {epoch} Summary | "
        f"Loss: {avg_loss:.4f} | CE: {avg_ce:.4f} | VLP: {avg_vlp:.4f}"
    )

    return avg_loss


@torch.no_grad()
def validate(
    agent_a: nn.Module,
    agent_b: nn.Module,
    loss_fn: Stage1Loss,
    loader: DataLoader,
    device: torch.device,
) -> float:
    """Run validation."""
    agent_a.eval()
    agent_b.eval()

    total_loss = 0.0

    for batch in loader:
        pixel_values = batch["pixel_values"].to(device)
        labels = batch["labels"].to(device)
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        text_features = batch["text_features"].to(device)

        a_output = agent_a(pixel_values)
        b_output = agent_b(
            pixel_values=None,
            visual_features=a_output.visual_features,
            input_ids=input_ids,
            attention_mask=attention_mask,
        )

        loss_output = loss_fn(
            logits=a_output.logits,
            labels=labels,
            visual_features=a_output.visual_features,
            text_features=text_features,
        )

        total_loss += loss_output.total.item()

    avg_loss = total_loss / len(loader)
    logger.info(f"Validation Loss: {avg_loss:.4f}")
    return avg_loss


def save_checkpoint(
    agent_a: nn.Module,
    agent_b: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    loss: float,
    checkpoint_dir: str,
    is_best: bool = False,
):
    """Save model checkpoint."""
    os.makedirs(checkpoint_dir, exist_ok=True)

    checkpoint = {
        "epoch": epoch,
        "agent_a_state_dict": agent_a.state_dict(),
        "agent_b_state_dict": agent_b.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "loss": loss,
    }

    filename = "stage1_best.pt" if is_best else f"stage1_epoch_{epoch}.pt"
    path = os.path.join(checkpoint_dir, filename)
    torch.save(checkpoint, path)
    logger.info(f"Checkpoint saved: {path}")


def main(args: argparse.Namespace):
    """Main training function for Stage 1."""
    # Load config
    config = load_config(args.config)
    t_cfg = config["training"]
    l_cfg = config["loss"]
    log_cfg = config["logging"]

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    logger.info(f"Using device: {device}")
    if device.type == "cuda":
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")

    # Set seed
    torch.manual_seed(config.get("seed", 42))
    if device.type == "cuda":
        torch.cuda.manual_seed_all(config.get("seed", 42))

    # Build models
    agent_a, agent_b = build_models(config, device)

    # Loss function
    loss_fn = Stage1Loss(
        weight_ce=l_cfg["weight_ce"],
        weight_vlp=l_cfg["weight_vlp"],
        temperature=l_cfg["temperature"],
    ).to(device)

    # Optimizer
    optimizer = build_optimizer(agent_a, agent_b, config)

    # Dataloaders
    train_loader, val_loader = build_dataloaders(config)

    # TensorBoard
    writer = SummaryWriter(log_dir=log_cfg["tensorboard_dir"])
    logger.info(f"TensorBoard logs: {log_cfg['tensorboard_dir']}")

    # Training loop
    best_val_loss = float("inf")

    for epoch in range(1, t_cfg["num_epochs"] + 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Epoch {epoch}/{t_cfg['num_epochs']}")
        logger.info(f"{'='*60}")

        # Train
        train_loss = train_epoch(
            agent_a=agent_a,
            agent_b=agent_b,
            loss_fn=loss_fn,
            optimizer=optimizer,
            loader=train_loader,
            device=device,
            epoch=epoch,
            writer=writer,
            log_interval=log_cfg["log_interval"],
            gradient_accumulation_steps=t_cfg["gradient_accumulation_steps"],
            max_grad_norm=t_cfg["max_grad_norm"],
        )

        # Validate
        if epoch % max(1, t_cfg["num_epochs"] // 4) == 0:
            val_loss = validate(agent_a, agent_b, loss_fn, val_loader, device)
            writer.add_scalar("val/loss", val_loss, epoch)

            # Save best
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                save_checkpoint(
                    agent_a, agent_b, optimizer, epoch, val_loss,
                    log_cfg["checkpoint_dir"], is_best=True,
                )

        # Regular checkpoint
        if epoch % max(1, t_cfg["num_epochs"] // 4) == 0:
            save_checkpoint(
                agent_a, agent_b, optimizer, epoch, train_loss,
                log_cfg["checkpoint_dir"],
            )

    writer.close()
    logger.info("Stage 1 training complete!")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Stage 1: Pre-train Agent A + Agent B"
    )
    parser.add_argument(
        "--config", type=str, default="configs/stage1.yaml",
        help="Path to config file",
    )
    parser.add_argument(
        "--cpu", action="store_true",
        help="Force CPU training",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
