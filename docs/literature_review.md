# Focused Literature Review: Video-Based Respiratory Monitoring

This short review frames the engineering choices in RespiratoryVision. It is not a systematic review.

## 1. Zhan et al. (2020) — Revisiting motion-based respiration measurement from videos

**Problem:** Estimate respiration from subtle chest/belly motion in video.  
**Method:** Motion-based video analysis evaluated under multiple practical challenges.  
**Relevance:** Supports the use of visible body motion as a contactless respiratory signal.  
**Design implication:** Begin with an interpretable motion baseline and explicitly test robustness.  
**Source:** PubMed PMID 33019319, DOI 10.1109/EMBC44109.2020.9175662

## 2. Gwak et al. (2022) — Motion-Based Respiratory Rate Estimation with Motion Artifact Removal

**Problem:** Motion artifacts can overwhelm respiratory motion.  
**Method:** Uses face/upper-chest regions with artifact removal and region selection.  
**Reported finding:** Chest-motion estimates were more accurate than head-only estimates in the reported experiments.  
**Design implication:** RespiratoryVision focuses its default ROI on the upper torso and reports signal quality.  
**Source:** PubMed PMID 36086435, DOI 10.1109/EMBC48229.2022.9871231

## 3. Rehouma et al. / pediatric pneumonia video monitoring literature

**Problem:** Measure respiratory rate and chest indrawing in children without intrusive sensors.  
**Method:** Extracts respiratory signals from RGB video and analyzes periodic chest-abdominal movement.  
**Design implication:** Pediatric respiratory monitoring makes privacy, motion robustness, and clinical validation especially important.  
**Source:** PubMed PMID 34715683

## 4. Real-time thoracoabdominal motion with consumer cameras

**Problem:** Recover respiratory rate from periodic thoracoabdominal movement in ordinary video.  
**Method:** Optical-flow-based motion estimation followed by respiratory-frequency analysis.  
**Design implication:** Optical flow is a strong, interpretable baseline for a student research prototype.  
**Source:** PubMed PMID 28268880

## 5. A simple remote video-based breathing monitor

**Problem:** Contactless breathing estimation using ordinary video.  
**Method:** Tracks points of interest with Lucas-Kanade optical flow and estimates a harmonic respiratory frequency.  
**Design implication:** Multiple tracked motion signals can later be fused to improve robustness.  
**Source:** PubMed PMID 29060235

## 6. Smartphone-based prospective respiratory-rate validation

**Problem:** Estimate respiratory rate from commodity RGB video.  
**Method:** Motion analysis using a face-derived upper-torso ROI.  
**Design implication:** Anatomy-aware ROI localization is a useful extension beyond the current geometric ROI.  
**Source:** Communications Medicine (2022), "Prospective validation of smartphone-based heart rate and respiratory rate measurement algorithms."

## 7. Video-Based Respiratory Rate Estimation for Infants in the NICU (2024)

**Problem:** Estimate infant respiratory rate from video in a clinically relevant environment.  
**Relevance:** Demonstrates the importance of neonatal/pediatric-specific validation and synchronized ground truth.  
**Design implication:** Synthetic validation cannot substitute for carefully governed clinical data.  
**Source:** PubMed PMID 39559825, DOI 10.1109/JTEHM.2024.3488523

## 8. Recent neonatal respiratory-monitoring work

Recent work has combined thoracoabdominal ROI segmentation, optical-flow motion extraction, detrending, peak detection, and movement-quality gating.

**Design implication:** A future RespiratoryVision iteration could add anatomy-aware segmentation and explicit movement rejection before respiratory estimation.

## Research gaps for this prototype

The present repository does not yet solve:
- automatic anatomy-aware ROI selection,
- large voluntary body motion,
- pediatric-specific pose variation,
- clinical ground-truth synchronization,
- multimodal fusion,
- uncertainty calibration,
- prospective clinical validation.

These are appropriate future research directions rather than claims of completed capability.
