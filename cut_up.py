import librosa
import os
import soundfile as sf

def cut_up_audio(base_path, folder):
    print('Analysing audio...')

    path = base_path + '/' + '/downloads/video-audio.mp3'
    y, sr = librosa.load(path)

    tempo, beat_frames = librosa.beat.beat_track(y=y,sr=sr)
    print(f'tempo: {tempo}')

    beat_samples = librosa.frames_to_samples(beat_frames)

    output_dir = base_path + '/' + folder
    os.makedirs(output_dir, exist_ok=True)

    targets = [
        (1, 1),
        (1, 2),
        (1, 3), 
        (1, 4), 
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (3, 1),
        (3, 2),
        (3, 3), 
        (3, 4), 
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        
    ]

    beat_duration = int(sr * 60 / tempo )
    half_beat_duration = beat_duration//2

    print('Cutting up audio...')

    for i, (bar, beat) in enumerate(targets):
        beat_index = (bar - 1) * 4 + (beat - 1)
        
        if beat_index >= len(beat_samples):
            print(f"Skipping: bar {bar}, beat {beat} — index out of range")
            continue

        start_sample = beat_samples[beat_index]
        end_sample = start_sample + beat_duration

        clip = y[start_sample:end_sample]
        output_path = os.path.join(output_dir, f"sample_{i}.wav")
        sf.write(output_path, clip, sr)
        print(f"Saved: {output_path}")