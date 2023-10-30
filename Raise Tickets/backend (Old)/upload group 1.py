import img_to_text
import upload_file
import video_compress
import choose_type_of_ticket

img_to_text.calibrate({'Group 1': {'paths': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715519.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715529.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715539.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715550.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/VID_20230721_144742 - Copy - Copy.mp4']}})
data = img_to_text.data
data['Group 1'] = choose_type_of_ticket.run(data['Group 1'])
upload_file.run_file(data['Group 1'], data['Group 1'][0])
