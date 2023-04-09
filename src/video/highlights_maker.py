import os
from moviepy.editor import VideoFileClip, concatenate_videoclips,vfx

class Highlight_Make:
    def highlight_maker(self, player_name, game_date, assets_path, build_path):

        #Read each file's name in the folder and put it in a list
        clip_list = os.listdir(f"{build_path}/{game_date}/{player_name}/clips")
        
        #Rerange the list with increasing order
        x = []
        for _ in clip_list:
            x.append(int(_.replace(".mp4","")))
        x.sort()

        ordered_clip_list = []
        for _ in x:
            ordered_clip_list.append(str(_)+".mp4")
        
        #Create transition for each clip and add it in a list
        new_clip_list = []

        for _ in ordered_clip_list:
            clip = VideoFileClip(f"{build_path}/{game_date}/{player_name}/clips/{_}").fx(vfx.fadein, 0.5).fx(vfx.fadeout, 0.5)
            new_clip_list.append(clip)

        #Import the prmotion ending video and add it to the list
        promotion_ending = VideoFileClip(f"{assets_path}/promotion/promotion_ending.mp4")
        new_clip_list.append(promotion_ending)

        #Concatenate all the clips to a highlights video
        final = concatenate_videoclips(new_clip_list)

        #Export the highlights video
        final.write_videofile(f"{build_path}/{game_date}/{player_name}/{player_name}.mp4")