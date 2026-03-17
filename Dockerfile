FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04

# System dependencies
RUN apt-get update && apt-get install -y \
curl git nano ca-certificates \
curl -fsSL https://claude.ai/install.sh | bash \
&& rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"

WORKDIR /workspace

CMD ["bash"]
