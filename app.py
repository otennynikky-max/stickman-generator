import os
import math
from gtts import gTTS
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from moviepy.editor import AudioFileClip, ImageSequenceClip, concatenate_videoclips
import gradio as gr

def make_viral_video(topic_input):
    scenes_data = [
        {"text": f"Today we are uncovering the hidden truth about {topic_input}.", "action": "zoom"},
        {"text": "Most people have no clue how this actually works behind closed doors.", "action": "favor"},
        {"text": "But if you look closely at the data, the pattern becomes obvious.", "action": "door"},
        {"text": "Stare at the facts long enough, and the illusions disappear.", "action": "stare"},
        {"text": f"That is the reality of {topic_input}. Subscribe for more daily breakdowns.", "action": "outro"}
    ]
    
    audio_clips = []
    scene_durations = []
    
    # 1. Voiceover Generation
    for i, scene in enumerate(scenes_data):
        filename = f"detailed_scene_{i}.mp3"
        tts = gTTS(text=scene["text"], lang='en', tld='com')
        tts.save(filename)
        audio_clip = AudioFileClip(filename)
        audio_clips.append(audio_clip)
        scene_durations.append(audio_clip.duration)

    WIDTH, HEIGHT = 1080, 1920
    FPS = 24
    video_clips = []

    # 2. Detailed Drawing Engine
    def draw_detailed_scene(draw, x, y, frame_idx, pose="normal", action="none"):
        # Draw a cinematic blueprint grid background
        grid_size = 80
        for i in range(0, WIDTH, grid_size):
            draw.line([i, 0, i, HEIGHT], fill="#224422", width=2)
        for j in range(0, HEIGHT, grid_size):
            draw.line([0, j, WIDTH, j], fill="#224422", width=2)

        # Main Stickman Structure (Thicker, clean comic lines)
        # Head Shadow & Head
        draw.ellipse([x-55, y-155, x+55, y-45], fill="#111111")
        draw.ellipse([x-50, y-150, x+50, y-50], fill="#FFFFFF", outline="black", width=12)
        
        # Expressive Animated Face
        if action == "zoom":
            # Glowing Evil/Smart Red Eyes
            draw.ellipse([x-25, y-115, x-5, y-95], fill="red")
            draw.ellipse([x+5, y-115, x+25, y-95], fill="red")
            # Sinister smirk mouth
            draw.arc([x-20, y-90, x+20, y-70], start=0, end=180, fill="black", width=5)
        elif action == "stare":
            # Giant shocked white eyes with tiny pupils
            draw.ellipse([x-30, y-120, x-5, y-90], fill="white", outline="black", width=3)
            draw.ellipse([x+5, y-120, x+30, y-90], fill="white", outline="black", width=3)
            draw.ellipse([x-20, y-108, x-14, y-102], fill="black")
            draw.ellipse([x+14, y-108, x+20, y-102], fill="black")
            # Open talking mouth that moves over time
            mouth_size = 5 + int(5 * math.sin(frame_idx * 0.8))
            draw.ellipse([x-10, y-80, x+10, y-80+mouth_size], fill="black")
        else:
            # Default Eyes & Moving Mouth
            draw.ellipse([x-20, y-110, x-10, y-100], fill="black")
            draw.ellipse([x+10, y-110, x+20, y-100], fill="black")
            # Talking Mouth sync animation
            if (frame_idx // 3) % 2 == 0:
                draw.line([x-15, y-80, x+15, y-80], fill="black", width=6)
            else:
                draw.ellipse([x-10, y-85, x+10, y-75], fill="black")

        # Body & Limbs (Thickened strokes for premium look)
        draw.line([x, y-5, x, y+160], fill="black", width=22) # Spine
        
        # Arm Poses
        if pose == "wave":
            draw.line([x, y+20, x-70, y+90], fill="black", width=16) # Left
            # Waving Right Arm
            wave_offset = int(25 * math.sin(frame_idx * 0.5))
            draw.line([x, y+20, x+70 + wave_offset, y-40], fill="black", width=16)
        elif pose == "point":
            draw.line([x, y+20, x-70, y+90], fill="black", width=16)
            draw.line([x, y+20, x+100, y+20], fill="black", width=16) # Pointing out
        else:
            # Standard Idle breathing arms
            breath = int(3 * math.sin(frame_idx * 0.2))
            draw.line([x, y+20, x-65, y+90 + breath], fill="black", width=16)
            draw.line([x, y+20, x+65, y+90 + breath], fill="black", width=16)
            
        # Legs
        draw.line([x, y+160, x-60, y+300], fill="black", width=18)
        draw.line([x, y+160, x+60, y+300], fill="black", width=18)

    # 3. Clip Assembly Engine
    for i, scene in enumerate(scenes_data):
        duration = scene_durations[i]
        total_frames = int(duration * FPS)
        frames = []
        
        for frame_idx in range(total_frames):
            # Rich aesthetic background color
            img = Image.new("RGB", (WIDTH, HEIGHT), "#0A1C0A")
            draw = ImageDraw.Draw(img)
            cx, cy = WIDTH // 2, HEIGHT // 2 + 100
            
            if scene["action"] == "zoom":
                draw_detailed_scene(draw, cx, cy, frame_idx, "wave", "zoom")
            elif scene["action"] == "favor":
                draw_detailed_scene(draw, cx - 180, cy, frame_idx, "normal", "none")
                draw_detailed_scene(draw, cx + 180, cy, frame_idx, "normal", "none")
                # Animated floating pop-art elements
                float_y = int(15 * math.sin(frame_idx * 0.3))
                draw.ellipse([cx-20, cy-150+float_y, cx+20, cy-110+float_y], fill="orange")
            elif scene["action"] == "door":
                draw_detailed_scene(draw, cx, cy, frame_idx, "point", "none")
            elif scene["action"] == "stare":
                shake = int(math.sin(frame_idx * 0.9) * 8)
                draw_detailed_scene(draw, cx - 180, cy, frame_idx, "normal", "none")
                draw_detailed_scene(draw, cx + 180 + shake, cy, frame_idx, "normal", "stare")
            else:
                draw_detailed_scene(draw, cx, cy, frame_idx, "normal", "none")
                
            frames.append(np.array(img))
            
        clip = ImageSequenceClip(frames, fps=FPS)
        clip = clip.set_audio(audio_clips[i])
        video_clips.append(clip)

    final_video = concatenate_videoclips(video_clips, method="compose")
    output_path = "viral_detailed_short.mp4"
    final_video.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac")
    
    return output_path

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎬 AI Stickman Video Generator Studio Pro")
    gr.Markdown("Type your niche topic to automatically render animated face elements and grid layouts.")
    
    with gr.Row():
        with gr.Column():
            topic_box = gr.Textbox(label="Video Topic Niche", placeholder="e.g., 3 Dark Psychology Tricks...")
            generate_btn = gr.Button("🚀 Generate HD Detailed Video", variant="primary")
        
        with gr.Column():
            video_preview = gr.Video(label="Your Finished Video Output")
            
    generate_btn.click(fn=make_viral_video, inputs=topic_box, outputs=video_preview)

demo.launch(server_name="0.0.0.0", server_port=7860)

