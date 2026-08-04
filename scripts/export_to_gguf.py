import os
import subprocess
import sys

MERGED_DIR = os.path.join("models", "merged_cyberguard")
F16_GGUF_OUTPUT = os.path.join("models", "cyberguard_f16.gguf")
GGUF_OUTPUT = os.path.join("models", "cyberguard_q4_k_m.gguf")

def convert_and_quantize():
    print(f"1️⃣ Converting merged HF model from '{MERGED_DIR}' to FP16 GGUF...")
    convert_script = os.path.join("llama.cpp", "convert_hf_to_gguf.py")
    
    # sys.executable ensures execution within your active venv
    subprocess.run(
        [
            sys.executable,
            convert_script,
            MERGED_DIR,
            "--outfile",
            F16_GGUF_OUTPUT,
            "--outtype",
            "f16",
        ],
        check=True,
    )

    print("2️⃣ Checking for quantizer executable...")
    quantize_bin = os.path.join("llama.cpp", "build", "bin", "Release", "llama-quantize.exe")
    if not os.path.exists(quantize_bin):
        quantize_bin = os.path.join("llama.cpp", "build", "bin", "llama-quantize")

    if os.path.exists(quantize_bin):
        subprocess.run(
            [quantize_bin, F16_GGUF_OUTPUT, GGUF_OUTPUT, "Q4_K_M"],
            check=True,
        )
        print(f"✅ Success! 4-bit GGUF model created at '{GGUF_OUTPUT}'")
    else:
        print(f"✅ FP16 GGUF created at '{F16_GGUF_OUTPUT}'!")
        print("💡 Note: 'llama-quantize' binary was not compiled, but you can use 'cyberguard_f16.gguf' directly in loader.py.")

if __name__ == "__main__":
    convert_and_quantize()