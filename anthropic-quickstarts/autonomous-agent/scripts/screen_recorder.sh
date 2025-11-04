#!/usr/bin/env bash
# Rolling screen recorder for the Raspberry Pi

set -euo pipefail

OUTPUT_DIR="${1:-data/recordings}"
MAX_SIZE_GB="${2:-10}"
FPS="${3:-2}"

mkdir -p "$OUTPUT_DIR"

echo "Starting screen recorder..."
echo "Output directory: $OUTPUT_DIR"
echo "Max size: ${MAX_SIZE_GB}GB"
echo "FPS: $FPS"

# Function to get directory size in GB
get_dir_size() {
    du -sb "$OUTPUT_DIR" | awk '{print $1 / 1024 / 1024 / 1024}'
}

# Function to delete oldest file
delete_oldest() {
    oldest=$(ls -t "$OUTPUT_DIR"/*.mp4 2>/dev/null | tail -1)
    if [ -n "$oldest" ]; then
        echo "Deleting oldest recording: $oldest"
        rm "$oldest"
    fi
}

# Start recording loop
while true; do
    timestamp=$(date +%Y%m%d_%H%M%S)
    output_file="$OUTPUT_DIR/recording_$timestamp.mp4"

    # Check size and cleanup if needed
    current_size=$(get_dir_size)
    while (( $(echo "$current_size > $MAX_SIZE_GB" | bc -l) )); do
        delete_oldest
        current_size=$(get_dir_size)
    done

    # Record for 1 hour (3600 seconds)
    echo "Recording to: $output_file"
    ffmpeg -video_size 1920x1080 -framerate $FPS -f x11grab -i :0.0 \
        -c:v libx264 -preset ultrafast -t 3600 "$output_file" 2>/dev/null || true

    echo "Segment complete, starting next..."
done
