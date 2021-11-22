import json
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Cloth
from django.db.models import Count

from django.conf import settings
from .forms import ClothForm

import numpy as np
import cv2
import torch
from cloths_segmentation.pre_trained_models import create_model
from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
import albumentations as albu


model2 = create_model("Unet_2020-10-30")






@login_required
def cloth_delete(request, pk, username):
    cloth = get_object_or_404(Cloth, pk=pk)
    user = get_object_or_404(get_user_model(), username=username)
    if cloth.author != request.user or request.method == 'GET':
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')

    if request.method == 'POST':
        cloth.delete()
        
        user_profile = user.profile
    
        
        cloth_list = user.cloth_set.all() 
    
        all_cloth_list = Cloth.objects.all
    
    
        return render(request, 'cloth/my_cloth_list.html', {
            'user_profile': user_profile,
            'cloth_list': cloth_list,
            'all_cloth_list': all_cloth_list,
            'username': username,
        })

        # messages.success(request, '삭제완료')
        # return redirect('cloth:my_cloth_list' user.username)
    


@login_required
def cloth_edit(request, pk, username):
    cloth = get_object_or_404(Cloth, pk=pk)

    user = get_object_or_404(get_user_model(), username=username)

    
    if request.method == 'POST':
        form = ClothForm(request.POST, request.FILES,instance=cloth)
        if form.is_valid():
            post = form.save()
            cloth.author = request.user
            
            cloth.save()
            
            user_profile = user.profile
    
        
            cloth_list = user.cloth_set.all() 
    
            all_cloth_list = Cloth.objects.all
            messages.success(request, '수정완료')
    
            return render(request, 'cloth/my_cloth_list.html', {
                'user_profile': user_profile,
                'cloth_list': cloth_list,
                'all_cloth_list': all_cloth_list,
                'username': username,
            })
            
            
            # return redirect('post:post_list')
    else:
        form = ClothForm()
    return render(request, 'cloth/cloth_edit.html', {
        'cloth': cloth,
        'form': form,
    })
    
    
    

def cloth_recommend(request, pk, username):
    
    cloth = get_object_or_404(Cloth, pk=pk)
    # user = get_object_or_404(get_user_model(), username=cloth.author.username)
    user = get_object_or_404(get_user_model(), username=username)
    user=cloth.author
    cloth_list = user.cloth_set.all() 
    reco_list=[];
    for c in cloth_list:
        print("+++++++++++++cloth_recommend++++++++++++++++")
        print(type(c.season))
        print(type(cloth.part))
        print(type('사계절'))
        if((c.season==cloth.season or cloth.season=='사계절' or c.season=='사계절') and c.part != cloth.part):
            print(c.season)
            print(c.part)
            reco_list.append(c)
    print("선택된옷: ")
    print(cloth)
    print("추천된옷: ")
    print(reco_list)
    
    return render(request, 'cloth/recommend.html', {
        
        'cloth': cloth,
        'reco_list':reco_list,
    })

def cloth_recommend_tit(request, pk, username):
    
    cloth = get_object_or_404(Cloth, pk=pk)
    # user = get_object_or_404(get_user_model(), username=cloth.author.username)
    user = get_object_or_404(get_user_model(), username=username)
    user=cloth.author
    cloth_list = user.cloth_set.all() 
    reco_list=[];
    for c in cloth_list:
        print("+++++++++++++cloth_recommend++++++++++++++++")
        print(type(c.season))
        print(type(cloth.part))
        print(type('사계절'))
        if((c.season==cloth.season or cloth.season=='사계절' or c.season=='사계절') and c.part != cloth.part):
            print(c.season)
            print(c.part)
            reco_list.append(c)
    print("선택된옷: ")
    print(cloth)
    print("추천된옷: ")
    print(reco_list)
    
    print("선택된옷 색상: ")
    print(cloth.r_color);
    print(cloth.g_color);
    print(cloth.b_color);
    cloth_color=[cloth.r_color,cloth.g_color,cloth.b_color]
    cloth_color=np.uint8(cloth_color)
    print(cloth_color);
    F=[]
    for i in range(0,180,30):
        x=i
        Z=np.array([ 
            [[x ,255,255],[x ,200 ,255],[x ,150 ,255],[x, 100 ,255],[x, 50, 255],[x ,0 ,255],
            [x ,255 ,255],[x, 255,200],[x ,255 ,150],[x ,255 ,100],[x, 255, 50],[x ,255 ,0]] 
            ])
        Z=np.uint8(Z)
        img = cv2.cvtColor(Z, cv2.COLOR_HSV2RGB)
                
        F.append(img)
                
    F1=np.vstack(F)
    tit=[]
    for i in range(F1.shape[0]):
        for j in range(F1.shape[1]):
            if(np.array_equal(F1[i,j], cloth_color)):
                for k in range(F1.shape[0]):
                    print(F1[k,j])
                    x=F1[k,j].reshape(1,1,3)
                    tit.append(x)
 

    print("톤인톤")
    tit=np.vstack(tit)
    tit=tit.reshape(-1,3)
    print(tit)
    
    print(tit.shape)
    tit_reco_list=[];
    for c in reco_list:
        print("+++++++++++++tit_recommend++++++++++++++++")
        reco_cloth_color=[c.r_color,c.g_color,c.b_color]
        reco_cloth_color=np.uint8(reco_cloth_color)
        # print(reco_cloth_color);
        for t in tit:
            
            if((reco_cloth_color[0]==t[0])and(reco_cloth_color[1]==t[1])and(reco_cloth_color[2]==t[2])):
                print(reco_cloth_color)
                print(t)
                tit_reco_list.append(c)
                print("선택된옷: ")
                print(c)
    print("톤온톤 추천된옷: ")
    print(tit_reco_list)
    
    return render(request, 'cloth/recommend.html', {
        
        'cloth': cloth,
        'reco_list':tit_reco_list,
    })

def cloth_recommend_tot(request, pk, username):
    
    cloth = get_object_or_404(Cloth, pk=pk)
    # user = get_object_or_404(get_user_model(), username=cloth.author.username)
    user = get_object_or_404(get_user_model(), username=username)
    user=cloth.author
    cloth_list = user.cloth_set.all() 
    reco_list=[];
    for c in cloth_list:
        print("+++++++++++++cloth_recommend++++++++++++++++")
        print(type(c.season))
        print(type(cloth.part))
        print(type('사계절'))
        if((c.season==cloth.season or cloth.season=='사계절' or c.season=='사계절') and c.part != cloth.part):
            print(c.season)
            print(c.part)
            reco_list.append(c)
    print("선택된옷: ")
    print(cloth)
    print("추천된옷: ")
    print(reco_list)
    
    print("선택된옷 색상: ")
    print(cloth.r_color);
    print(cloth.g_color);
    print(cloth.b_color);
    cloth_color=[cloth.r_color,cloth.g_color,cloth.b_color]
    cloth_color=np.uint8(cloth_color)
    print(cloth_color);
    F=[]
    for i in range(0,180,30):
        x=i
        Z=np.array([ 
            [[x ,255,255],[x ,200 ,255],[x ,150 ,255],[x, 100 ,255],[x, 50, 255],[x ,0 ,255],
            [x ,255 ,255],[x, 255,200],[x ,255 ,150],[x ,255 ,100],[x, 255, 50],[x ,255 ,0]] 
            ])
        Z=np.uint8(Z)
        img = cv2.cvtColor(Z, cv2.COLOR_HSV2RGB)
                
        F.append(img)
                
    F1=np.vstack(F)
    tot=[]
    for i in range(F1.shape[0]):
        for j in range(F1.shape[1]):
            if(np.array_equal(F1[i,j],cloth_color)):
                for k in range(F1.shape[1]):
                    print(F1[i,k])
                    x=F1[i,k].reshape(1,1,3)
                    tot.append(x)
            
            
    print("톤온톤")
    tot=np.vstack(tot)
    tot=tot.reshape(-1,3)
    print(tot)
    
    print(tot.shape)
    tot_reco_list=[];
    for c in reco_list:
        print("+++++++++++++tot_recommend++++++++++++++++")
        reco_cloth_color=[c.r_color,c.g_color,c.b_color]
        reco_cloth_color=np.uint8(reco_cloth_color)
        # print(reco_cloth_color);
        for t in tot:
            
            if((reco_cloth_color[0]==t[0])and(reco_cloth_color[1]==t[1])and(reco_cloth_color[2]==t[2])):
                print(reco_cloth_color)
                print(t)
                tot_reco_list.append(c)
                print("선택된옷: ")
                print(c)
    print("톤온톤 추천된옷: ")
    print(tot_reco_list)
    
    return render(request, 'cloth/recommend.html', {
        
        'cloth': cloth,
        'reco_list':tot_reco_list,
    })


def my_cloth_list(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    user_profile = user.profile
    
        
    cloth_list = user.cloth_set.all() 
    
    all_cloth_list = Cloth.objects.all
    
    # image = load_rgb("/workspace/since9697_fashion/since9697/media/cloth/2021/11/10/jyj1143/clTBvEvO.jpg")
    # transform = albu.Compose([albu.Normalize(p=1)], p=1)
    # padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)
    # x = transform(image=padded_image)["image"]
    # x = torch.unsqueeze(tensor_from_rgb_image(x), 0)
    # with torch.no_grad():
    #     prediction = model2(x)[0][0]
    # mask = (prediction > 0).cpu().numpy().astype(np.uint8)
    # mask = unpad(mask, pads)

    
    return render(request, 'cloth/my_cloth_list.html', {
        'user_profile': user_profile,
        'cloth_list': cloth_list,
        'all_cloth_list': all_cloth_list,
        'username': username,
    })




@login_required
def cloth_new(request):
    if request.method == 'POST':
        form = ClothForm(request.POST, request.FILES)
        if form.is_valid():
            cloth = form.save(commit=False)
            cloth.author = request.user
            
            cloth.save()
            
            imageURL = settings.MEDIA_URL + form.instance.photo.name
            path = '/workspace/since9697_fashion/since9697' + imageURL
            print("=====================================")
            print(path)
            image=cv2.imread(path, cv2.IMREAD_UNCHANGED)
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            print(path+form.instance.photo.name)
            image = load_rgb(path)
            transform = albu.Compose([albu.Normalize(p=1)], p=1)
            padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)
            x = transform(image=padded_image)["image"]
            x = torch.unsqueeze(tensor_from_rgb_image(x), 0)
            with torch.no_grad():
                prediction = model2(x)[0][0]
            mask = (prediction > 0).cpu().numpy().astype(np.uint8)
            mask = unpad(mask, pads)
            # dst = cv2.addWeighted(image, 1, (cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) * (0, 255, 0)).astype(np.uint8), 0.5, 0)
            
            img2= cv2.add(image,(~(cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) * 255)))
            img2= cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)    
            
            img3= cv2.multiply(image,((cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB))))
            img3= cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
            
            alpha=(mask*255)
            r, g, b = cv2.split(img2)
            rgba = [r,g,b, alpha]
            dst = cv2.merge(rgba,4)
            # dst = cv2.merge((r,g,b, alpha))
            print("=====================================")
            print(dst.shape)
            
            # gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path, dst)
            messages.info(request, '새 글이 등록되었습니다')
            
            
            
            #색인식
            img = cv2.imread(path)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            cv2.imwrite(path, image)

            # img2= cv2.add(image,(~(cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) * 255)))
            # img=dst
            print(img.shape)
            print(type(img))
            arr=[]

            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # myimg=np.empty((2, 2, 3), int)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            channels = cv2.split(img)

            colors = ['r', 'g', 'b']
            for ch, color in zip(channels, colors):
    
                hist = cv2.calcHist([ch], [0], mask, [256], [0, 256])
    
                print(np.argmax(hist))
                arr.append(np.argmax(hist))

            
            print("R G B")
            print(arr)
            # form.instance.create(r_color=100, g_color=100,b_color=100)  
            
            
            F=[]
            for i in range(0,180,30):
                x=i
              # print(x)
                Z=np.array([ 
                      [[x ,255,255],[x ,200 ,255],[x ,150 ,255],[x, 100 ,255],[x, 50, 255],[x ,0 ,255],
                      [x ,255 ,255],[x, 255,200],[x ,255 ,150],[x ,255 ,100],[x, 255, 50],[x ,255 ,0]] 
                      ])
                Z=np.uint8(Z)
                img = cv2.cvtColor(Z, cv2.COLOR_HSV2RGB)
                
                F.append(img)
                
            F1=np.vstack(F)
            F2=np.hstack(F)
            F2=F2.reshape(-1,3)

            xy1=np.array(
                [
                    [arr]
                ])
            x1=0;
            x2=x1+30;
            x3=x2+30;
            x4=x3+30;
            x5=x4+30;
            x6=x5+30;

            xy2=np.array(F2)


            mindist=np.zeros(len(xy1))
            minid=np.zeros(len(xy1))
            print(xy1)
            print(xy2)
            # print(minid.shape)


            
            for i,xy in enumerate(xy1):
                dists=np.array(np.sum((xy-xy2)**2,axis=1))
                print(dists)
                mindist[i],minid[i]=dists.min(),dists.argmin()
                print(mindist[i])
                minid[i]=dists.argmin()
                print(minid[i])

            
            print("========================================")
            print(mindist)
            print(minid)
            
            minid = np.array(minid, dtype=np.int8)
            print(minid)
            print(arr)
            print(F2[minid][0])
            
            
            
            #색저장
            cloth.r_color=F2[minid][0][0]
            cloth.g_color=F2[minid][0][1]
            cloth.b_color=F2[minid][0][2]
            cloth.save()
            
            return redirect('post:post_list')
    else:
        form = ClothForm()
    return render(request, 'cloth/cloth_new.html', {
        'form': form,
    })

