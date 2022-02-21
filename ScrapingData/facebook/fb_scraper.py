from facebook_scraper import get_posts
import pandas as pd


get_post = get_posts('PrabowoSubianto', pages=20,options={"comments": True})
post_id = []
text = []
post_text = []
shared_text = []
time= []
timestamp = []
image = []
image_lowquality = []
images = []
images_description = []
images_lowquality = []
images_lowquality_description = []
video = []
video_duration_seconds = []
video_height = []
video_id = []
video_quality = []
video_size_MB = []
video_thumbnail = []
video_watches = []
video_width = []
likes = []
comments = []
shares = []
post_url = []
link = []
links = []
user_id = []
username = []
user_url = []
is_live = []
shared_post_id = []
shared_time = []
shared_user_id = []
shared_username = []
shared_post_url = []
available = []
comments_full = []
reactors = []
w3_fb_url = []
reactions = []
reaction_count = []
page_id = []
sharers = []
image_id = []
image_ids = []
was_live = []

for data in get_post:
    post_id.append(data.get('append'))
    text.append(data.get('text'))
    post_text.append(data.get('post_text'))
    shared_text.append(data.get('shared_text'))
    time.append(data.get('time'))
    timestamp.append(data.get('timestamp'))
    image.append(data.get('image'))
    image_lowquality.append(data.get('image_lowquality'))
    images.append(data.get('images'))
    images_description.append(data.get('images_description'))
    images_lowquality.append(data.get('images_lowquality'))
    images_lowquality_description.append(data.get('images_lowquality_description'))
    video.append(data.get('video'))
    video_duration_seconds.append(data.get('video_duration_seconds'))
    video_height.append(data.get('video_height'))
    video_id.append(data.get('video_id'))
    video_quality.append(data.get('video_quality'))
    video_size_MB.append(data.get('video_size_MB'))
    video_thumbnail.append(data.get('video_thumbnail'))
    video_watches.append(data.get('video_watches'))
    video_width.append(data.get('video_widt'))
    likes.append(data.get('likes'))
    comments.append(data.get('comments'))
    shares.append(data.get('shares'))
    post_url.append(data.get('post_url'))
    link.append(data.get('link'))
    links.append(data.get('links'))
    user_id.append(data.get('user_id'))
    username.append(data.get('username'))
    user_url.append(data.get('user_url'))
    is_live.append(data.get('is_live'))
    shared_post_id.append(data.get('shared_post_id'))
    shared_time.append(data.get('shared_time'))
    shared_user_id.append(data.get('shared_user_id'))
    shared_username.append(data.get('shared_username'))
    shared_post_url.append(data.get('shared_post_url'))
    available.append(data.get('available'))
    comments_full.append(data.get('comments_full'))
    reactors.append(data.get('reactors'))
    w3_fb_url.append(data.get('w3_fb_url'))
    reactions.append(data.get('reactions'))
    reaction_count.append(data.get('reaction_count'))
    page_id.append(data.get('page_id'))
    sharers.append(data.get('sharers'))
    image_id.append(data.get('image_id'))
    image_ids.append(data.get('image_ids'))
    was_live.append(data.get('was_live'))

df = pd.DataFrame({'post_id':post_id,
                    'text':text,
                    'post_text':post_text,
                    'shared_text':shared_text,
                    'time':time,
                    'timestamp':timestamp,
                    'image':image,
                    'image_lowquality':image_lowquality,
                    'images':images,
                    'images_description':images_description,
                    'images_lowquality':images_lowquality,
                    'images_lowquality_description':images_lowquality_description,
                    'video':video,
                    'video_duration_seconds':video_duration_seconds,
                    'video_height':video_height,
                    'video_id':video_id,
                    'video_quality':video_quality,
                    'video_size_MB':video_size_MB,
                    'video_thumbnail':video_thumbnail,
                    'video_watches':video_watches,
                    'video_width':video_width,
                    'likes':likes,
                    'comments':comments,
                    'shares':shares,
                    'post_url':post_url,
                    'link':link,
                    'links':links,
                    'user_id':user_id,
                    'username':username,
                    'user_url':user_url,
                    'is_live':is_live,
                    'shared_post_id':shared_post_id,
                    'shared_time':shared_time,
                    'shared_user_id':shared_user_id,
                    'shared_username':shared_username,
                    'shared_post_url':shared_post_url,
                    'available':available,
                    'comments_full':comments_full,
                    'reactors':reactors,
                    'w3_fb_url':w3_fb_url,
                    'reactions':reactions,
                    'reaction_count':reaction_count,
                    'page_id':page_id,
                    'sharers':sharers,
                    'image_id':image_id,
                    'image_ids':image_ids,
                    'was_live':was_live})

df.to_excel("data indihome.xlsx")
print("mining complete")