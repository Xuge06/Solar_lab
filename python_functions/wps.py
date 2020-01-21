def wps_SG2(location, date_begin, date_end, dt):
    # location: geopoint [lat lon elev]
    # date_begin: datetime
    # date_end: datetime
    # dt: time step (hour)

    import uuid
    import os
    import pandas
    from datetime import datetime
    from datetime import timedelta
    from urllib.request import urlopen

    if (len(location) == 2):
        location[3] = -999;

    #unique id
    uid = uuid.uuid4().hex

    fic_output_csv = 'compute_sun_position_output_{}.csv'.format(uid)

    nd = int((date_end-date_begin).total_seconds()/(dt*3600))+1

    str_wps = 'http://toolbox.webservice-energy.org/service/wps?Service=WPS&Request=Execute&Identifier=ComputeSunPosition&version=1.0.0&RawDataOutput=result&DataInputs=';
    datainputs_wps = 'latitude={:.6f};longitude={:.6f};altitude={:.1f};offset={};count={:d};increment={:.12f}'.format(location[0], location[1], location[2],date_begin.strftime('%Y-%m-%dT%H:%M:%S'),nd, dt/24);
    
    response = urlopen('{}{}'.format(str_wps,datainputs_wps))
    SG2 = pandas.read_csv(response,delimiter=';',comment='#',header=None,names=["JDUT","YYYY","MM","DD","H","DOY","DELTA","OMEGA","GAMMA_S0","ALPHA_S","R"])
    
    return SG2
    
def wps_CAMS_RAD(location, date_begin, date_end, dt, email):
    # location: geopoint [lat lon elev]
    # date_begin: datetime
    # date_end: datetime
    # dt: time step (hour)
    # email: username(email) in soda-pro.com (string)

    import uuid
    import os
    import pandas
    from datetime import datetime
    from datetime import timedelta
    from urllib.request import urlopen

    dt60_to_duration = {1: "PT01M", 15: "PT15M", 60: "PT01H", 1440: "P01D"}

    if (len(location) == 2):
        location[3] = -999;

    #unique id
    uid = uuid.uuid4().hex

    fic_output_csv = 'get_cams_rad_output_{}.csv'.format(uid)

    str_wps = 'http://www.soda-is.com/service/wps?Service=WPS&Request=Execute&Identifier=get_cams_radiation&version=1.0.0&RawDataOutput=irradiation&DataInputs='
    datainputs_wps = 'latitude={:.6f};longitude={:.6f};altitude={:.1f};date_begin={};date_end={};time_ref=UT;summarization={};username={}'\
	.format(location[0], location[1], location[2],date_begin.strftime('%Y-%m-%d'),date_end.strftime('%Y-%m-%d'),dt60_to_duration.get(int(dt*60),"PT60M"),email.replace("@","%2540"));
    
    print(datainputs_wps)
    response = urlopen('{}{}'.format(str_wps,datainputs_wps))
    CAMS = pandas.read_csv(response,delimiter=';',comment='#',header=None,names=['TOA', 'CLEAR_SKY_GHI', 'CLEAR_SKY_BHI', 'CLEAR_SKY_DHI', 'CLEAR_SKY_BNI', 'GHI', 'BHI','DHI','BNI','Reliability'])
     
    return CAMS
    
def wps_Horizon_SRTM(location):
    # location: geopoint [lat lon elev]

    import uuid
    import os
    import pandas
    from urllib.request import urlopen

    if (len(location) == 2):
        location[3] = -999;

    #unique id
    uid = uuid.uuid4().hex

    fic_output_csv = 'horizon_srtm_output_{}.csv'.format(uid)

    str_wps = 'http://toolbox.webservice-energy.org/service/wps?service=WPS&request=Execute&identifier=compute_horizon_srtm&version=1.0.0&DataInputs=';
    datainputs_wps = 'latitude={:.6f};longitude={:.6f};altitude={:.1f}'\
	.format(location[0], location[1], location[2]);
    
    print(datainputs_wps)
    response = urlopen('{}{}'.format(str_wps,datainputs_wps))
    HZ = pandas.read_csv(response,delimiter=';',comment='#',header=None,skiprows=16,nrows=360,names=['AZIMUT', 'ELEVATION'])
     
    return HZ