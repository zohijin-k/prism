from models.schemas import AnalysisResult

MOCK_RESULT = AnalysisResult(
    summary={
        "problem": "This paper addresses the difficulty of accurately segmenting small objects in complex visual scenes.",
        "limitation": "Existing encoder-decoder architectures often lose fine-grained boundary information.",
        "method": "The proposed method introduces an attention-based skip connection module to preserve important spatial features.",
        "result": "The method improves Dice Score and mIoU compared to the baseline U-Net architecture.",
        "contribution": [
            "Attention-based feature refinement",
            "Improved boundary preservation",
            "Better reproducibility through modular architecture",
        ],
    },
    implementationPlan=[
        "Prepare dataset and define preprocessing pipeline",
        "Implement encoder-decoder model architecture",
        "Add attention module to skip connections",
        "Implement Dice Loss and BCE Loss",
        "Write training loop and validation loop",
        "Evaluate using Dice Score and mIoU",
        "Compare reproduced results with paper tables",
    ],
    components={
        "dataset": "Medical image segmentation dataset",
        "model": "Attention U-Net",
        "backbone": "U-Net encoder-decoder",
        "loss": "Dice Loss + BCE Loss",
        "optimizer": "Adam",
        "metrics": ["Dice Score", "mIoU"],
        "hyperparameters": {
            "learningRate": "1e-4",
            "batchSize": "8",
            "epochs": "100",
        },
    },
    comparison=[
        {
            "item": "Model Architecture",
            "paper": "Attention U-Net",
            "code": "AttentionUNet class found",
            "status": "Match",
        },
        {
            "item": "Loss Function",
            "paper": "Dice Loss + BCE Loss",
            "code": "DiceBCELoss implemented",
            "status": "Match",
        },
        {
            "item": "Optimizer",
            "paper": "Adam",
            "code": "Adam optimizer used in train.py",
            "status": "Match",
        },
        {
            "item": "Augmentation",
            "paper": "Not clearly specified",
            "code": "RandomFlip and RandomRotate found",
            "status": "Code Only",
        },
    ],
    mapping=[
        {
            "codeBlock": "models/attention_unet.py > AttentionGate",
            "paperSection": "Section 3.2 Attention Module",
            "paperReference": "Figure 2",
            "explanation": "This class appears to implement the attention gate described in the method section.",
            "confidence": "High",
        },
        {
            "codeBlock": "losses/dice_bce_loss.py > DiceBCELoss",
            "paperSection": "Section 3.4 Training Objective",
            "paperReference": "Equation 4",
            "explanation": "This loss function matches the training objective described in the paper.",
            "confidence": "High",
        },
        {
            "codeBlock": "train.py > optimizer = Adam(...)",
            "paperSection": "Experiment Setup",
            "paperReference": "Training Details",
            "explanation": "The optimizer configuration matches the experimental setup.",
            "confidence": "Medium",
        },
    ],
    missingInfo=[
        "Random seed is not specified in the paper.",
        "Learning rate scheduler is not clearly described.",
        "Detailed augmentation policy is missing.",
        "Pretrained weight usage is unclear.",
        "Exact GPU environment is not provided.",
    ],
)
