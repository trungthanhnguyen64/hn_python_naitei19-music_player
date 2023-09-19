from django.shortcuts import render
from catalog.models import Song,Listenlater ,UserSong,Playlist
from django.shortcuts import redirect
from django.utils.html import escape
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import F
from django.shortcuts import get_object_or_404

def usersong(request):
    """to record a listen history and return the user's history"""
    if request.method == "POST" :
        # dd(request)
        song_id = request.POST['song']
        user = request.user
        song = Song.objects.filter(id = song_id).first()
        # dd(song)
        usersong = UserSong(user = user , song = song )
        usersong.save()
        return redirect(f"/catalog/songs/{song_id}")
    history = UserSong.objects.filter(user = request.user)
    # dd(history)
    return render(request,'catalog/usersong.html',{"history":history})

def listenlater(request):
    if request.method == "POST" :
        # dd(request)
        listen_id = request.POST['listen_id']
        addll = Song.objects.filter(id = request.POST['listen_id']).first()
        # dd(addll)
        # for i in listen:
        #     dd(i.id)
        user = request.user
        # dd(user)
        listen = Listenlater.objects.filter(user=user)
        # dd(listen)
        for i in listen:
            if addll == i.listen:
                # message = "Your video is already added"
                break
        else:
            # dd(1)
            listenlater = Listenlater(user = user , listen = addll)
            listenlater.save()
            # message = "Your video is successfully added"
        # song = Song.objects.filter( id = listen_id)
        # return render(request,"song_page/songpost.html/", {"id": listen_id})
        
        return redirect(f"/catalog/songs/{listen_id}")
        
    
    ll = Listenlater.objects.filter(user = request.user)

    return render(request,'catalog/listenlater.html',{"song":ll})
    
def playlistdisplay(request, id):
    playlist_id = id
    playlist = Playlist.objects.filter(id = playlist_id).first()
    # songs = playlist.songs.all()
    # dd(songs)
    # dd(playlist)
    return render(request, 'catalog/playlist_details.html', {'playlist':playlist})

def playlist(request):
    playlist = Playlist.objects.all()
    return render(request,'catalog/playlist.html', {'playlist': playlist})

def creatplaylist(request):
    name = ""
    owner = ""
    image = None

    if request.method == "POST":
        # dd(request)
        name = request.POST.get('name')  
        current_user = request.user
        owner = current_user
        image = request.POST.get('image')  
        
        if name and owner:  
            
            song_model = Playlist(name=name, owner=owner, image=image)
            song_model.save()
            return redirect(f"/catalog/creatplaylist/")  

    return render(request, "catalog/creatplaylist.html")

def index(request):
    song = Song.objects.all()
    return render(request, 'catalog/index.html', {'song': song})

def songs(request):
    song = Song.objects.all()
    playlist = Playlist.objects.filter(owner = request.user)
    # dd(playlist)
    return render(request, 'song_page/song_page.html', {'song': song, 'playlists': playlist})
# {'song': song}: can co cai nay, o day de tra bien song ve 'song_page/song_page.html' duoi dang object ten la 'song'. Cai o trong '' la ten bien ma o muon tra n ve, cai sau dau : la bien o muon tra ve

def songpost(request, id):
    song = Song.objects.get(pk = id)
    # dd(song)
    song.listen_count = F('listen_count') + 1
    song.save()
    return render(request, 'song_page/songpost.html', {'song': song})

def search(request):
    query = request.GET.get("query")
    qs = Song.objects.filter(name__icontains=query)
    return render(request, 'song_page/search.html', {"songs": qs})

# def upload(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         artist = request.POST['artist']
#         image = request.FILES['file']
#         content = request.FILES['file']
    
#     song_model = Song(name=name ,artist=artist)
#     song_model.save()

#     return render(request,"catalog/upload.html")

def upload(request):
    name = ""
    artist = ""
    image = None
    content = None
    # rq = request
    print(request)
    if request.method == "POST":
        name = request.POST.get('name')  
        current_user = request.user
        artist = current_user
        image = request.FILES['image']  
        content = request.FILES['content'] 
        if name and artist :  
            
            song_model = Song.objects.create(name=name, artist=artist, image=image, content=content)
            song_model.save()
            
            return redirect(f"/catalog/upload/")  

    return render(request, "catalog/upload.html")
    
def addtoplaylist(request):
    if request.method == "POST":
        # dd(request)
        song_id = request.POST['song_id']
        playlist_id = request.POST['playlist_id']
        song = Song.objects.filter(id = song_id).first()
        playlist = Playlist.objects.filter(id = playlist_id).first()
        playlist.songs.add(song)
        return redirect(f"/catalog/songs/")

def trending(request):
    trending = Song.objects.all().order_by('-listen_count')
    return render(request, 'catalog/trending.html', {'trending': trending})
