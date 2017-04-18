from django.contrib.auth.models import User

from .models import UserProfile
from posts.models import Post


def build_users():
    # User 1 - mehtamanan
    manan = User.objects.create_user(username='mehtamanan', password='Manan123#', first_name='Manan', last_name='Mehta')
    manan.is_superuser = True
    manan.is_staff = True
    manan.email = 'mehtamanan@icloud.com'
    manan.save()

    # User 2 - poojag
    pooja = User.objects.create_user(username='poojag', password='Manan123#', first_name='Pooja', last_name='Ganatra')
    pooja.email = 'poojaganatra1997@gmail.com'
    pooja.save()

    # User 3 - tanyas
    tanya = User.objects.create_user(username='tanyas', password='Manan123#', first_name='Tanya', last_name='Singh')
    tanya.email = 'tstanya10@gmail.com'
    tanya.save()

    # User 5 - bang
    bang = User.objects.create_user(username='bang', password='Manan123#', first_name='Aniket', last_name='Bang')
    bang.email = 'bang.aniket@gmail.com'
    bang.save()

    # User 4 - chutiya
    shitty = User.objects.create_user(username='shitty', password='Manan123#', first_name='Khsitij', last_name='Jain')
    shitty.email = 'jainkshitij16@yahoo.com'
    shitty.save()

    # User 6 - sona
    sona = User.objects.create_user(username='sona', password='Manan123#', first_name='Jagriti', last_name='Sharma')
    sona.email = 'jagritisharma@hotmail.com'
    sona.save()

    # UserProfile for user 1
    me = UserProfile()
    me.user = manan
    me.bio = 'Computer scientist'
    me.birth_date = '1997-04-18'
    me.gender = 'M'
    me.save()

    # Userprofile for user 2
    poojag = UserProfile()
    poojag.user = pooja
    poojag.bio = 'Hot stuff'
    poojag.birth_date = '1997-08-09'
    poojag.gender = 'F'
    poojag.save()

    # UserProfile for user 3
    tans = UserProfile()
    tans.user = tanya
    tans.bio = 'Non-punjabi singh'
    tans.birth_date = '1997-12-24'
    tans.gender = 'F'
    tans.save()

    # UserProfile for user 5
    shit = UserProfile()
    shit.user = shitty
    shit.bio = 'idgaf'
    shit.birth_date = '1997-12-24'
    shit.gender = 'M'
    shit.save()

    # UserProfile for user 5
    mrbang = UserProfile()
    mrbang.user = bang
    mrbang.bio = 'Lame'
    mrbang.birth_date = '1996-06-11'
    mrbang.save()

    # Userprofile for user 6
    jags = UserProfile()
    jags.user = sona
    jags.bio = 'Non-badass'
    jags.birth_date = '1997-04-02'
    jags.gender = 'F'
    jags.save()

    # Post 1
    post = Post()
    post.owner = poojag
    post.movie_title = 'Inception'
    post.movie_id = 27205
    post.caption = 'To dream a little bigger'
    post.save()

    # Post 2
    post = Post()
    post.owner = me
    post.movie_title = 'Star Wars: The Force Awakens'
    post.movie_id = 140607
    post.caption = 'May the force be with you'
    post.save()

    # Post 3
    post = Post()
    post.owner = poojag
    post.movie_title = '12 angry men'
    post.movie_id = 389
    post.caption = "He's not guilty"
    post.save()

    # Post 4
    post = Post()
    post.owner = tans
    post.movie_title = 'The Prestige'
    post.movie_id = 1124
    post.caption = 'Are you watching closely?'
    post.save()

    # Post 5
    post = Post()
    post.owner = tans
    post.movie_title = 'Se7en'
    post.movie_id = 807
    post.caption = 'Seven deadly sins'
    post.save()

    # Post 6
    post = Post()
    post.owner = mrbang
    post.movie_title = 'The Dark Knight'
    post.movie_id = 49026
    post.caption = ''
    post.save()

    # Post 7
    post = Post()
    post.owner = poojag
    post.movie_title = 'Secondhand Lions'
    post.movie_id = 13156
    post.caption = "This is Sheriff Brady. I'm afraid I have some bad news for you. It's about your uncles."
    post.save()

    # Post 8
    post = Post()
    post.owner = poojag
    post.movie_title = '12 monkeys'
    post.movie_id = 63
    post.caption = 'Brad Pitt masterpiece!'
    post.save()

    # Post 9
    post = Post()
    post.owner = poojag
    post.movie_title = 'Fight club'
    post.movie_id = 550
    post.caption = "I found freedom. Losing all hope was freedom."
    post.save()

    tans.follow(username='mehtamanan')
    mrbang.follow(username='mehtamanan')
    jags.follow(username='mehtamanan')
    poojag.follow(username='mehtamanan')
    me.follow(username='poojag')
    me.follow(username='sona')
    me.follow(username='tanyasingh')
    tans.follow(username='bangbang')
    jags.follow(username='tanyasingh')
    jags.follow(username='bangbang')
    mrbang.follow(username='sona')
    jags.follow(username='poojag')
