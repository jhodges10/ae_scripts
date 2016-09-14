import os, subprocess, time

input_dir = raw_input("Enter your input directory path: ")
stills_dir = raw_input("Enter the directory for the output stills: ")

folder_list = os.listdir(input_dir)

FFMPEG_PATH = '/usr/local/bin/ffmpeg' # path to ffmpeg bin


for each_clip in folder_list:
    screen_shot = os.path.split(each_clip)
    screen_shot_fn = screen_shot[1]
    screen_shot_fn = screen_shot_fn.split('.')
    screen_shot_fn = screen_shot_fn[0]
    output_fn = screen_shot_fn
    each_clip = input_dir + '/' + each_clip
    output_filename = stills_dir + '/' + output_fn + '.jpg'
    subprocess.call([FFMPEG_PATH, '-ss', '1', '-i', each_clip, '-t', '1', '-s', '2048x1152', '-f', 'image2', output_filename])
    print output_fn
    time.sleep(.1)
    
print 'Done'


