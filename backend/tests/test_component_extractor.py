"""
Validation suite for the v1.1 extraction-precision update. No real PDFs are available for
these five papers, so each fixture is built directly in parse_pdf()'s output shape
({"full_text", "sections"}) with realistic Title/Abstract/Method/Related Work text, exercising
extract_components() the same way routers/analyze.py does after parse_pdf() succeeds.
"""

from component_extractor import extract_components

SECTION_HEADERS = {
    "abstract": "Abstract",
    "introduction": "Introduction",
    "related_work": "Related Work",
    "method": "Method",
    "implementation_details": "Implementation Details",
    "experiments": "Experiments",
    "results": "Results",
    "conclusion": "Conclusion",
}


def make_parsed(title: str, **section_bodies: str) -> dict:
    """Build a parse_pdf()-shaped dict from a title line plus named section bodies."""
    sections = {
        key: {"header": SECTION_HEADERS[key], "body": body}
        for key, body in section_bodies.items()
        if body
    }
    chunks = [title]
    for key, body in section_bodies.items():
        if body:
            chunks.append(f"{SECTION_HEADERS[key]}\n{body}")
    return {"full_text": "\n\n".join(chunks), "sections": sections}


def test_dcpnet_proposed_model_wins_over_related_work():
    parsed = make_parsed(
        "DCPNet: Deformable Control Point Network for Image Enhancement",
        abstract=(
            "Image enhancement remains challenging under real-world degradations. We propose "
            "DCPNet, a deformable control point network for image enhancement that learns to "
            "warp local control points to selectively enhance degraded regions. Extensive "
            "experiments show DCPNet achieves state-of-the-art performance."
        ),
        introduction=(
            "Image enhancement has been widely studied in recent years. In this paper, we "
            "introduce DCPNet to address the limitations of prior work."
        ),
        related_work=(
            "Early approaches such as U-Net and ViT laid the groundwork for image restoration. "
            "ResNet based backbones have also been explored for enhancement tasks. Unlike these "
            "methods, DCPNet employs deformable control points instead of fixed convolutions."
        ),
        method=(
            "The proposed DCPNet consists of an encoder and a deformable control point "
            "predictor. DCPNet first extracts multi-scale features from the degraded input. "
            "DCPNet then integrates a control point regression module to warp local regions."
        ),
        implementation_details=(
            "We train DCPNet using the Adam optimizer with a learning rate of 1e-4 and a batch "
            "size of 16 for 200 epochs."
        ),
        experiments="We evaluate DCPNet on the LOL dataset against several baselines.",
    )

    result = extract_components(parsed)

    assert result["model"]["value"] == "DCPNet"
    assert result["model"]["found"] is True
    assert result["task"]["value"] == "Image Enhancement"
    assert result["expandedModelName"] == "Deformable Control Point Network"
    assert "U-Net" in result["referencedModels"]
    assert "ViT" in result["referencedModels"]
    assert "ResNet" in result["referencedModels"]
    # Related-Work baselines must never become the primary model.
    assert result["model"]["value"] not in ("U-Net", "ViT", "ResNet")


def test_unet_is_its_own_proposed_model():
    parsed = make_parsed(
        "U-Net: Convolutional Networks for Biomedical Image Segmentation",
        abstract=(
            "There is large consent that successful training of deep networks requires many "
            "thousand annotated training samples. We present a network and training strategy "
            "that relies on the strong use of data augmentation, which is called u-net "
            "architecture. We show that such a network can be trained end-to-end from very few "
            "images to outperform prior methods."
        ),
        introduction=(
            "In this paper, we build upon a more elegant architecture, the so called fully "
            "convolutional network, which we call u-net."
        ),
        related_work=(
            "Prior segmentation approaches used sliding-window CNN classifiers and Faster R-CNN "
            "based detectors. Our u-net differs by using skip connections between the "
            "contracting and expanding paths."
        ),
        method=(
            "The u-net architecture is illustrated in Figure 1. It consists of a contracting "
            "path and an expansive path with skip connections. The u-net has no fully connected "
            "layers."
        ),
        implementation_details=(
            "We train u-net using stochastic gradient descent with a batch size of 1 due to GPU "
            "memory constraints, for 100 epochs."
        ),
    )

    result = extract_components(parsed)

    assert result["model"]["value"] == "U-Net"
    assert result["model"]["found"] is True


def test_segment_anything_multiword_name():
    parsed = make_parsed(
        "Segment Anything",
        abstract=(
            "We introduce Segment Anything, a new task, model, and dataset for image "
            "segmentation. We call this approach Segment Anything, also referred to as SAM. "
            "Our proposed Segment Anything model generalizes to novel objects without "
            "additional training. Extensive experiments show Segment Anything achieves strong "
            "zero-shot performance."
        ),
        related_work=(
            "Interactive segmentation has previously relied on U-Net style encoder-decoder "
            "architectures. DeepLab has also been used for semantic segmentation benchmarks."
        ),
        method=(
            "The Segment Anything model consists of an image encoder, a prompt encoder, and a "
            "mask decoder. Segment Anything is designed to be promptable, enabling zero-shot "
            "transfer to new tasks."
        ),
        experiments="Segment Anything is evaluated on the SA-1B dataset using the AdamW optimizer.",
    )

    result = extract_components(parsed)

    assert result["model"]["value"] == "Segment Anything"
    assert result["model"]["found"] is True
    assert "U-Net" in result["referencedModels"]


def test_clip_reversed_acronym_definition():
    parsed = make_parsed(
        "Learning Transferable Visual Models From Natural Language Supervision",
        abstract=(
            "State-of-the-art computer vision systems are trained to predict a fixed set of "
            "predetermined object categories. We demonstrate that predicting which caption "
            "goes with which image is an efficient way to learn image representations from "
            "scratch. We call this approach CLIP (Contrastive Language-Image Pre-training). "
            "CLIP learns directly from raw text about images, enabling zero-shot transfer to "
            "downstream tasks."
        ),
        related_work=(
            "Prior work such as VGG and ResNet learned visual representations from labeled "
            "ImageNet categories rather than natural language supervision."
        ),
        method=(
            "CLIP jointly trains an image encoder and a text encoder to predict the correct "
            "pairings of a batch of image-text training examples. At test time, CLIP performs "
            "zero-shot classification by embedding the names of the target classes."
        ),
        experiments="CLIP is trained using the Adam optimizer on a large corpus of image-text pairs.",
    )

    result = extract_components(parsed)

    assert result["model"]["value"] == "CLIP"
    assert result["model"]["found"] is True
    assert result["expandedModelName"] == "Contrastive Language-Image Pre-training"
    assert "VGG" in result["referencedModels"]
    assert "ResNet" in result["referencedModels"]


def test_resnet_known_term_fallback():
    parsed = make_parsed(
        "Deep Residual Learning for Image Recognition",
        abstract=(
            "Deeper neural networks are more difficult to train. We present a residual "
            "learning framework to ease the training of networks that are substantially deeper "
            "than those used previously. We provide comprehensive empirical evidence showing "
            "that these residual networks, which we refer to as ResNet, are easier to optimize "
            "and can gain accuracy from considerably increased depth."
        ),
        related_work=(
            "Prior architectures such as VGG and GoogLeNet use deeper stacks of small "
            "convolutional filters to improve accuracy on ImageNet."
        ),
        method=(
            "ResNet stacks multiple residual blocks, each containing shortcut connections that "
            "skip one or more layers. We build ResNet architectures with depths of 34, 50, 101, "
            "and 152 layers. Table 1 summarizes the ResNet variants used in our experiments."
        ),
        implementation_details=(
            "We train ResNet using SGD with a momentum of 0.9, a mini-batch size of 256, for 90 "
            "epochs."
        ),
    )

    result = extract_components(parsed)

    assert result["model"]["value"] == "ResNet"
    assert result["model"]["found"] is True
    assert "VGG" in result["referencedModels"]
    assert result["model"]["value"] != "VGG"


def test_optimizer_ignores_related_work_only_mentions():
    parsed = make_parsed(
        "ExampleNet: A Toy Architecture for Testing",
        abstract="We propose ExampleNet for the target task.",
        related_work="Unlike SGD used in prior work [12], our method uses a different scheme.",
        method="ExampleNet is trained end-to-end.",
        implementation_details="We optimize ExampleNet using the Adam optimizer.",
    )

    result = extract_components(parsed)

    assert result["optimizer"]["value"] == "Adam"
    assert result["optimizer"]["source"] == "implementation_details"
