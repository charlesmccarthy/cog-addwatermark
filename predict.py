from cog import BasePredictor, Input, Path
import subprocess
import argparse
import os


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")
    def predict(
        self,
        video: Path = Input(description="Input video"),
        size: int = Input(
            description="Size of font", ge=1, le=500, default=40
        ),
        watermark: str = Input(
            description="Watermark Text", default="FULLJOURNEY.AI"
        )
    ) -> Path:
        """Run a single prediction on the model"""
        # processed_input = preprocess(image)
        # output = self.model(processed_image, scale)
        # return postprocess(output)





        font_path = "Anton-Regular.ttf"  # Replace with the correct path to the Anton-Regular.ttf font file


        # Prepare output file path
        base, ext = os.path.splitext(str(video))
        output_video = Path(f"{base}_watermarked{ext}")

        # Construct ffmpeg command
        ffmpeg_command = [
            "ffmpeg", "-y", "-i", str(video), "-vf", 
            f"drawtext=text='{watermark}':fontfile={font_path}:fontsize={size}:fontcolor=white@0.5:x=(w-tw)-10:y=(h-th)-10",
            "-codec:a", "copy", str(output_video)
        ]

        # Execute the command
        subprocess.run(ffmpeg_command, check=True)

        if not output_video.exists():
            raise FileNotFoundError(f"Failed to create watermarked video at {output_video}")

        print(f"Watermarked video saved to {output_video}")
        return output_video
