from django.contrib.auth.models import User

from .models import UserProfile, Post


def build_users():
    # User 1 - mehtamanan
    user = User.objects.create_user(username='mehtamanan', password='Manan123#', first_name='Manan', last_name='Mehta')
    user.is_superuser = True
    user.is_staff = True
    user.email = 'mehtamanan@icloud.com'
    user.save()

    # User 2 - poojag
    user = User.objects.create_user(username='poojag', password='Pooja123#', first_name='Pooja', last_name='Ganatra')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'poojaganatra1997@gmail.com'
    user.save()

    # User 3 - tanyasingh24
    user = User.objects.create_user(username='tanyasingh', password='Tanya123#', first_name='Tanya', last_name='Singh')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'tstanya10@gmail.com'
    user.save()

    # User 4 - thejoker
    user = User.objects.create_user(username='thejoker', password='Arjun123#', first_name='Arjun', last_name='Sharma')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'arjunrocks1997@gmail.com'
    user.save()

    # User 5 - bangbang
    user = User.objects.create_user(username='bangbang', password='Bang123#', first_name='Aniket', last_name='Bang')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'bang.aniket@gmail.com'
    user.save()

    # User 6 - JagritiSonaSharma
    user = User.objects.create_user(username='sona', password='Sona123#', first_name='Jagriti', last_name='Sharma')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'jagritisharma@hotmail.com'
    user.save()

    # UserProfile for user 1
    user_profile = UserProfile()
    user_profile.user = User.objects.get(username='mehtamanan')
    user_profile.bio = 'Computer scientist'
    user_profile.birth_date = '1997-04-18'
    user_profile.save()

    # Userprofile for user 2
    user_profile = UserProfile()
    user_profile.user = User.objects.get(username='poojag')
    user_profile.bio = 'Hot stuff'
    user_profile.birth_date = '1997-08-09'
    user_profile.save()

    # UserProfile for user 3
    user_profile = UserProfile()
    user_profile.user = User.objects.get(username='tanyasingh')
    user_profile.bio = 'Non-punjabi singh'
    user_profile.birth_date = '1997-12-24'
    user_profile.save()

    # Userprofile for user 4
    user_profile = UserProfile()
    user_profile.user = User.objects.get(username='thejoker')
    user_profile.bio = 'Non-drinking Punjabi'
    user_profile.birth_date = '1997-08-09'
    user_profile.save()

    # UserProfile for user 5
    user_profile = UserProfile()
    user_profile.user = User.objects.get(username='bangbang')
    user_profile.bio = 'Lame'
    user_profile.birth_date = '1996-06-11'
    user_profile.save()

    # Userprofile for user 6
    user_profile = UserProfile()
    user_profile.user = User.objects.get(username='sona')
    user_profile.bio = 'Non-badass'
    user_profile.birth_date = '1997-04-02'
    user_profile.save()

    # Post 1
    post = Post()
    post.owner = User.objects.get(username='poojag').profile
    post.movie_title = 'Inception'
    post.movie_id = 'tt1375666'
    post.caption = 'To dream a little bigger'
    post.save()

    # Post 2
    post = Post()
    post.owner = User.objects.get(username='mehtamanan').profile
    post.movie_title = 'Star Wars: The Force Awakens'
    post.movie_id = 'tt2488496'
    post.caption = 'May the force be with you'
    post.save()

    # Post 3
    post = Post()
    post.owner = User.objects.get(username='poojag').profile
    post.movie_title = '12 angry men'
    post.movie_id = 'tt050083'
    post.caption = "He's not guilty"
    post.save()

    # Post 4
    post = Post()
    post.owner = User.objects.get(username='thejoker').profile
    post.movie_title = 'The Prestige'
    post.movie_id = 'tt0482571'
    post.caption = 'Are you watching closely?'
    post.save()

    # Post 5
    post = Post()
    post.owner = User.objects.get(username='tanyasingh').profile
    post.movie_title = 'Se7en'
    post.movie_id = 'tt0114369'
    post.caption = 'Seven deadly sins'
    post.save()

    # Post 6
    post = Post()
    post.owner = User.objects.get(username='thejoker').profile
    post.movie_title = 'The Dark Knight'
    post.movie_id = 'tt0468569'
    post.caption = ''
    post.save()

    # Post 7
    post = Post()
    post.owner = User.objects.get(username='poojag').profile
    post.movie_title = 'Secondhand Lions'
    post.movie_id = 'tt0327137'
    post.caption = "This is Sheriff Brady. I'm afraid I have some bad news for you. It's about your uncles."
    post.save()

    # Post 8
    post = Post()
    post.owner = User.objects.get(username='poojag').profile
    post.movie_title = '12 monkeys'
    post.movie_id = 'tt0114746'
    post.caption = 'Brad Pitt masterpiece!'
    post.save()

    # Post 9
    post = Post()
    post.owner = User.objects.get(username='poojag').profile
    post.movie_title = 'Fight club'
    post.movie_id = 'tt0137523'
    post.caption = "I found freedom. Losing all hope was freedom."
    post.save()

    User.objects.get(username='tanyasingh').profile.follow(username='mehtamanan')
    User.objects.get(username='bangbang').profile.follow(username='mehtamanan')
    User.objects.get(username='sona').profile.follow(username='mehtamanan')
    User.objects.get(username='poojag').profile.follow(username='mehtamanan')
    User.objects.get(username='thejoker').profile.follow(username='mehtamanan')
    User.objects.get(username='mehtamanan').profile.follow(username='poojag')
    User.objects.get(username='mehtamanan').profile.follow(username='sona')
    User.objects.get(username='thejoker').profile.follow(username='tanyasingh')
    User.objects.get(username='tanyasingh').profile.follow(username='thejoker')
    User.objects.get(username='tanyasingh').profile.follow(username='bangbang')
    User.objects.get(username='sona').profile.follow(username='tanyasingh')
    User.objects.get(username='sona').profile.follow(username='bangbang')
    User.objects.get(username='bangbang').profile.follow(username='sona')
    User.objects.get(username='sona').profile.follow(username='poojag')
