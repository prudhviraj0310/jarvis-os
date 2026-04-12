import os
import time

class VisionEngine:
    """
    Phase Y: Visual Perception Stack.
    Combines Raw Screen Capture (mss) and Object Character Recognition (pytesseract) 
    to map semantic text to X/Y coordinates for the LLM.
    Falls back gracefully if dependencies are missing.
    """
    def __init__(self):
        self._mss = None
        self._pytesseract = None
        self._pil = None
        self._deps_available = False
        self._ensure_deps()

    def _ensure_deps(self):
        """Try loading real vision deps. Gracefully degrade if missing."""
        try:
            import mss
            self._mss = mss
        except ImportError:
            pass
        
        try:
            import pytesseract
            self._pytesseract = pytesseract
        except ImportError:
            pass
        
        try:
            from PIL import Image
            self._pil = Image
        except ImportError:
            pass

        if self._mss and self._pytesseract and self._pil:
            self._deps_available = True
            print("[VisionEngine] Optical Nerve Stack online (mss + pytesseract).")
        else:
            missing = []
            if not self._mss: missing.append("mss")
            if not self._pytesseract: missing.append("pytesseract")
            if not self._pil: missing.append("Pillow")
            print(f"[VisionEngine] Running in degraded mode. Missing: {', '.join(missing)}")

    def capture_screen(self, save_path="/tmp/jarvis_vision_latest.png"):
        """
        Takes a physical snapshot of the active Linux session.
        Uses mss for high-performance screen capture.
        """
        if self._mss:
            try:
                with self._mss.mss() as sct:
                    monitor = sct.monitors[1]  # Primary monitor
                    screenshot = sct.grab(monitor)
                    # Convert to PIL Image and save
                    img = self._pil.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                    img.save(save_path)
                    print(f"[VisionEngine] 📸 Screen captured ({screenshot.size[0]}x{screenshot.size[1]})")
                    return save_path
            except Exception as e:
                print(f"[VisionEngine] Screen capture failed: {e}")
        
        print("[VisionEngine] 📸 Screen capture unavailable (no mss). Using stub.")
        return save_path

    def process_ocr(self, image_path: str) -> dict:
        """
        Runs pytesseract against the capture to extract bounding boxes.
        Returns a dictionary mapping text to [X, Y, W, H] coordinates.
        """
        if self._pytesseract and self._pil and os.path.exists(image_path):
            try:
                img = self._pil.open(image_path)
                # Get bounding box data with position info
                data = self._pytesseract.image_to_data(img, output_type=self._pytesseract.Output.DICT)
                
                visual_map = {}
                n_boxes = len(data['text'])
                for i in range(n_boxes):
                    text = data['text'][i].strip()
                    conf = int(data['conf'][i])
                    # Only include confident text detections (>60% confidence, >2 chars)
                    if conf > 60 and len(text) > 2:
                        visual_map[text] = {
                            "x": data['left'][i],
                            "y": data['top'][i],
                            "w": data['width'][i],
                            "h": data['height'][i]
                        }
                
                print(f"[VisionEngine] 👁️ OCR extracted {len(visual_map)} text regions.")
                return visual_map
            except Exception as e:
                print(f"[VisionEngine] OCR processing failed: {e}")
        
        # Fallback: return empty map (no mock data)
        print("[VisionEngine] 👁️ OCR unavailable. No visual data.")
        return {}

    def look(self) -> dict:
        """
        The master entry method for the perception pipeline.
        Invokes Screen Capture -> OCR -> Semantic Geometry mapping.
        """
        img_path = self.capture_screen()
        visual_map = self.process_ocr(img_path)
        return visual_map
