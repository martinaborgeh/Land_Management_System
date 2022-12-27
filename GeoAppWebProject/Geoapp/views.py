from ast import boolop
from django.shortcuts import render,redirect
from .form import RegistrationForm,DetailsForm
from django.contrib import messages
from . models import Boundary
from django.contrib.gis.geos import Polygon
import pyproj as prj





def basehtmlrender(request):
    return render(request,"base.html")

def registration(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = RegistrationForm()
    data = {'form':form}
    return render(request,"register.html",data)


def GetDetailsFromUSer(request):
    detail_form=DetailsForm()
    if request.method =='POST':
            formdata1,formdata2,formdata3 = request.POST.get('Parcel_ID_1'),request.POST.get('Parcel_ID_2'),request.POST.get('Parcel_ID_3')
            if formdata1 !='' and formdata2=='' and formdata3=='':
                queried = Boundary.objects.filter(ParcelId=formdata1).values_list()
                if queried:
                    details = {'queried':queried[0]}
                    northings,eastings = details['queried'][9::2],details['queried'][10::2]
                    zipped =list(zip([data for data in northings if isinstance(data,float)],[data1 for data1 in eastings if isinstance(data1,float)]))
                    natinal_grid =[list(data) for data in zipped]
                    json_data ={'polygon_data1':coordinate_transform(zipped)}
                    json_data['nationalGrid']=natinal_grid
                    json_data['owner_details']=Boundary.objects.get(id =details['queried'][8])
                    print(Boundary.objects.get(id =details['queried'][8]).OwnerPhoto)
                    return render(request,"DisplayBoundaryDetails.html",json_data)
                else:
                    json_data ={'message':f' The {formdata1} is found'}
                    return render (request,'wrongid.html',json_data)
            elif formdata1 =='' and formdata2 != '' and formdata3 =='':
                queried = Boundary.objects.filter(ParcelId=formdata2).values_list()
                if queried:
                    details = {'queried':queried[0]}
                    northings,eastings =details['queried'][9::2],details['queried'][10::2]
                    zipped =list(zip([data for data in northings if isinstance(data,float)],[data1 for data1 in eastings if isinstance(data1,float)]))
                    natinal_grid =[list(data) for data in zipped]
                    json_data ={'polygon_data1':coordinate_transform(zipped)}
                    json_data['nationalGrid']=natinal_grid
                    json_data['owner_details']=Boundary.objects.get(id =details['queried'][8])
                    return render(request,"DisplayBoundaryDetails.html",json_data)
                else:
                    json_data ={'message':f' The {formdata2} is found'}
                    return render (request,'wrongid.html',json_data)
            elif formdata1 =='' and formdata2 == '' and formdata3 !='':
                queried = Boundary.objects.filter(ParcelId=formdata3).values_list()
                if queried:
                    details = {'queried':queried[0]}
                    northings,eastings =details['queried'][9::2],details['queried'][10::2] 
                    zipped =list(zip([data for data in northings if isinstance(data,float)],[data1 for data1 in eastings if isinstance(data1,float)]))
                    natinal_grid =[list(data) for data in zipped]
                    json_data ={'polygon_data1':coordinate_transform(zipped)}
                    json_data['nationalGrid']=natinal_grid
                    json_data['owner_details']=Boundary.objects.get(id =details['queried'][8])
                    return render(request,"DisplayBoundaryDetails.html",json_data)
                else:
                    json_data ={'message':f' The {formdata3} is found'}
                    return render (request,'wrongid.html',json_data)
            elif formdata1 !='' and formdata2 != '' and formdata3 =='':
                queried1,queried2 = Boundary.objects.filter(ParcelId=formdata1).values_list(),Boundary.objects.filter(ParcelId=formdata2).values_list() 
                if queried1 and queried2:
                    json_data={}
                    detail1,detail2 = {'queried1':queried1[0]},{'queried2':queried2[0]}
                    northing1,easting1 =detail1['queried1'][9::2],detail1['queried1'][10::2]
                    northing2,easting2 =detail2['queried2'][9::2],detail2['queried2'][10::2]
                    zipped1,zipped2 =list(zip([data for data in northing1 if isinstance(data,float)],[data1 for data1 in easting1 if isinstance(data1,float)])),\
                    list(zip([data for data in northing2 if isinstance(data,float)],[data1 for data1 in easting2 if isinstance(data1,float)]))
                    natinal_grid1,natinal_grid2 =[list(data) for data in zipped1],[list(data) for data in zipped2]
                    json_data['polygon_data1']=coordinate_transform(zipped1)
                    json_data['polygon_data2']=coordinate_transform(zipped2)
                    json_data['nationalGrid1']=natinal_grid1
                    json_data['nationalGrid2']=natinal_grid2
                    json_data['owner_detail1']=Boundary.objects.get(id =detail1['queried1'][8])
                    json_data['owner_detail2']=Boundary.objects.get(id =detail2['queried2'][8])
                    return render(request,"DisplayBoundaryDetails.html",json_data)
                elif not queried1 and queried2 :
                    json_data ={'message':f' The {formdata1} is not found'}
                    return render (request,'wrongid.html',json_data)
                elif queried1 and not queried2:
                    json_data ={'message':f' The {formdata2} is not found'}
                    return render (request,'wrongid.html',json_data)

                else:
                    json_data ={'message':f' The {formdata1} and {formdata2} are not found'}
                    return render (request,'wrongid.html',json_data)
            elif formdata1 =='' and formdata2 != '' and formdata3 !='':
                queried2,queried3 = Boundary.objects.filter(ParcelId=formdata2).values_list(),Boundary.objects.filter(ParcelId=formdata3).values_list()
                if queried2 and queried3:
                    json_data={}
                    detail2,detail3 = {'queried2':queried2[0]},{'queried3':queried3[0]}
                    northing2,easting2 =detail2['queried2'][9::2],detail2['queried2'][10::2]
                    northing3,easting3 =detail3['queried3'][9::2],detail3['queried3'][10::2]
                    zipped2,zipped3 =list(zip([data for data in northing2 if isinstance(data,float)],[data1 for data1 in easting2 if isinstance(data1,float)])),\
                     list(zip([data for data in northing3 if isinstance(data,float)],[data1 for data1 in easting3 if isinstance(data1,float)]))
                    natinal_grid2,natinal_grid3 =[list(data) for data in zipped2],[list(data) for data in zipped3]
                    json_data['polygon_data1']=coordinate_transform(zipped2)
                    json_data['polygon_data2']=coordinate_transform(zipped3)
                    json_data['nationalGrid1']=natinal_grid2
                    json_data['nationalGrid2']=natinal_grid3
                    json_data['owner_detail1']=Boundary.objects.get(id =detail2['queried2'][8])
                    json_data['owner_detail2']=Boundary.objects.get(id =detail3['queried3'][8])
                    return render(request,"DisplayBoundaryDetails.html",json_data)
                elif not queried2 and queried3:
                    json_data ={'message':f' The {formdata2} is not found'}
                    return render (request,'wrongid.html',json_data)
                elif queried2 and not queried3:
                    json_data ={'message':f' The {formdata3} is not found'}
                    return render (request,'wrongid.html',json_data)
                else:
                    json_data ={'message':f' The {formdata3} and {formdata2} are not found'}
                    return render (request,'wrongid.html',json_data)
            elif formdata1 !='' and formdata2 == '' and formdata3 !='':
                queried1,queried3 = Boundary.objects.filter(ParcelId=formdata1).values_list(),Boundary.objects.filter(ParcelId=formdata3).values_list()
                if queried1 and queried3:
                    json_data={}
                    detail1,detail3 = {'queried1':queried1[0]},{'queried3':queried3[0]}
                    northing1,easting1 =detail1['queried1'][9::2],detail1['queried1'][10::2]
                    northing3,easting3 =detail3['queried3'][9::2],detail3['queried3'][10::2] 
                    zipped1,zipped3  =list(zip([data for data in northing1 if isinstance(data,float)],[data1 for data1 in easting1 if isinstance(data1,float)])),\
                    list(zip([data for data in northing3 if isinstance(data,float)],[data1 for data1 in easting3 if isinstance(data1,float)]))
                    natinal_grid1,natinal_grid3  =[list(data) for data in zipped1],[list(data) for data in zipped3]
                    json_data['polygon_data1']=coordinate_transform(zipped1)
                    json_data['polygon_data2']=coordinate_transform(zipped3)
                    json_data['nationalGrid1']=natinal_grid1
                    json_data['nationalGrid2']=natinal_grid3
                    json_data['owner_detail1']=Boundary.objects.get(id =detail1['queried1'][8])
                    json_data['owner_detail2']=Boundary.objects.get(id =detail3['queried3'][8])
                    return render(request,"DisplayBoundaryDetails.html",json_data)
                elif not queried1 and queried3:
                   json_data ={'message':f' The {formdata1} is not found'}
                   return render (request,'wrongid.html',json_data)
                elif queried1 and not queried3:
                    json_data ={'message':f' The {formdata3} is not found'}
                    return render (request,'wrongid.html',json_data)
                else:
                    json_data ={'message':f' The {formdata1} and {formdata3} are not found'}
                    return render (request,'wrongid.html',json_data)
            elif formdata1 !='' and formdata2 != '' and formdata3 !='':
                queried1,queried2,queried3 = Boundary.objects.filter(ParcelId=formdata1).values_list(),Boundary.objects.filter(ParcelId=formdata2).values_list(),Boundary.objects.filter(ParcelId=formdata3).values_list()
                if queried1 and queried2 and queried3:
                    json_data={}
                    detail1,detail2 = {'queried1':queried1[0]},{'queried2':queried2[0]}
                    detail3 = {'queried3':queried3[0]}
                    northing1,easting1 =detail1['queried1'][9::2],detail1['queried1'][10::2] 
                    northing2,easting2 =detail2['queried2'][9::2],detail2['queried2'][10::2]
                    northing3,easting3 =detail3['queried3'][9::2],detail3['queried3'][10::2]
                    zipped1,zipped2,zipped3 =list(zip([data for data in northing1 if isinstance(data,float)],[data1 for data1 in easting1 if isinstance(data1,float)])),\
                    list(zip([data for data in northing2 if isinstance(data,float)],[data1 for data1 in easting2 if isinstance(data1,float)])),\
                    list(zip([data for data in northing3 if isinstance(data,float)],[data1 for data1 in easting3 if isinstance(data1,float)]))
                    natinal_grid1,natinal_grid2,natinal_grid3 =[list(data) for data in zipped1],[list(data) for data in zipped2],[list(data) for data in zipped3]
                    json_data['polygon_data1']=coordinate_transform(zipped1)
                    json_data['polygon_data2']=coordinate_transform(zipped2)
                    json_data['polygon_data3']=coordinate_transform(zipped3)
                    json_data['nationalGrid1']=natinal_grid1
                    json_data['nationalGrid2']=natinal_grid2
                    json_data['nationalGrid3']=natinal_grid3
                    json_data['owner_detail1']=Boundary.objects.get(id =detail1['queried1'][8])
                    json_data['owner_detail2']=Boundary.objects.get(id =detail2['queried2'][8])
                    json_data['owner_detail3']=Boundary.objects.get(id =detail3['queried3'][8])
                    return render(request,"DisplayBoundaryDetails.html",json_data)
                elif queried1 and queried2 and not queried3:
                    json_data ={'message':f' The {formdata3} is not found'}
                    return render (request,'wrongid.html',json_data)
                elif queried2 and queried3 and not queried1:
                    json_data ={'message':f' The {formdata1} is not found'}
                    return render (request,'wrongid.html',json_data)
                elif queried1 and queried3 and not queried2:
                    json_data ={'message':f' The {formdata2} is not found'}
                    return render (request,'wrongid.html',json_data)
                elif not queried1  and queried2  and not queried3:
                    json_data ={'message':f' The {formdata1} and {formdata3} is not found'}
                    return render (request,'wrongid.html',json_data)
                elif queried1 and not queried2 and not queried3:
                    json_data ={'message':f' The {formdata2} and {formdata3} is not found'}
                    return render (request,'wrongid.html',json_data)
                elif not queried1  and not queried2 and queried3:
                    json_data ={'message':f' The {formdata1} and {formdata2} is not found'}
                    return render (request,'wrongid.html',json_data)
                else:
                    json_data ={'message':f' The {formdata1} , {formdata2} and {formdata3}  are not found'}
                    return render (request,'wrongid.html',json_data)
            
            else:
                json_data ={'message':f'Make an entry of a parcel id or more into the entry space provided'}
                return render(request,'wrongid.html',json_data)
            
        
            
    else:detail_form = DetailsForm()
    context = {'searchform':detail_form}    
    return render(request,"SearchBoundaryDetails.html",context)


def sendDetailsToUser(request):
     return render(request,"DisplayBoundaryDetails.html")


def homepage(request):
    return render(request,'homepage.html')


def profile(request):
    return render(request,'profile.html')


def wrongparcelid(request):
    return render(request,'wrongid.html')


def coordinate_transform(national_grid_coordinate):
    projection = prj.Transformer.from_crs(2136,4326)
    return [list(projection.transform(values[0],values[1])) for values in national_grid_coordinate]
    





    

    
    




