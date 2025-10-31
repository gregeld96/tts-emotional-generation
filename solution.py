"""
AI Dev Challenge — Emotional Speech Generation
TTS prototype in Python using Coqui TTS

Usage:
  python solution.py "Hello world"
  python solution.py "Hello world" --style enthusiastic --out hello.wav
"""

import sys
import argparse
import os
from pathlib import Path
from TTS.api import TTS # type: ignore

def main():
    parser = argparse.ArgumentParser(description="Simple Emotional TTS using Coqui")
    parser.add_argument("text", type=str, nargs="?", help="Text to synthesize")
    parser.add_argument("--style", type=str, default="neutral",
                        choices=["neutral", "enthusiastic"],
                        help="Speech style (neutral or enthusiastic)")
    parser.add_argument("--out", type=str, default="output.wav", help="Output .wav file name")
    args = parser.parse_args()

    # handle empty text
    if not args.text or args.text.strip() == "":
        print("Error: Please provide a non-empty text string.")
        sys.exit(1)
    
    # Validate output file extension (.wav only)
    output_path = Path(args.out)
    if output_path.suffix.lower() != ".wav":
        print(f"Error: Invalid output format '{output_path.suffix}'. Only '.wav' files are allowed.")
        sys.exit(1)

    # Validate and prepare output path
    try:
        output_dir = output_path.parent

        # Create directory if it doesn't exist
        if not output_dir.exists():
            print(f"Creating directory: {output_dir}")
            output_dir.mkdir(parents=True, exist_ok=True)

        # Check write permission
        if not os.access(output_dir, os.W_OK):
            print(f"Error: No write permission for directory: {output_dir}")
            sys.exit(1)

        # Warn if file exists
        if output_path.exists():
            print(f"Warning: File {args.out} already exists and will be overwritten.")

    except Exception as e:
        print(f"Error validating output path '{args.out}': {e}")
        sys.exit(1)

    # Load model
    model_name = "tts_models/en/ljspeech/tacotron2-DDC"
    print(f"🔄 Loading model: {model_name}")
    
    try:
        tts = TTS(model_name)
    except Exception as e:
        print(f"Error loading TTS model: {e}")
        sys.exit(1)

    # Adjust parameters based on emotion
    if args.style == "neutral":
        speed = 1.0
    elif args.style == "enthusiastic":
        speed = 1.2
    else:
        speed = 1.0

    print(f"🎵 Generating '{args.style}' speech → {args.out}")
    
    # Generate speech
    try:
        tts.tts_to_file(text=args.text, file_path=args.out, speed=speed)
        
        # Verify the file was actually created
        if Path(args.out).exists() and Path(args.out).stat().st_size > 0:
            file_size = Path(args.out).stat().st_size / 1024
            print(f"Success! Audio file saved: {args.out} ({file_size:.1f} KB)")
        else:
            print("Error: Output file was not created or is empty")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n Operation cancelled by user")
        # Clean up partial file if it exists
        if Path(args.out).exists():
            Path(args.out).unlink()
        sys.exit(1)
    except Exception as e:
        print(f"Error generating speech: {e}")
        # Clean up partial file if it exists
        if Path(args.out).exists():
            Path(args.out).unlink()
        sys.exit(1)

if __name__ == "__main__":
    main()
