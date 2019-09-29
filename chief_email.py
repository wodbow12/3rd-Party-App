#-*- coding: utf-8 -*-
import os,sys
import smtplib, datetime
import urllib2
import io
sys.path.insert(0, '/core/TD/shotgunAPI/python-api-master')
import shotgun_api3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import  MIMEImage

def registerCallbacks(reg):
    """
    Register our callbacks.
    :param reg: A Registrar instance provided by the event loop handler.
    """

    # Grab authentication env vars for this plugin. Install these into the env
    # if they don't already exist.
    server = os.environ["SG_SERVER"]
    script_name = os.environ["SGDAEMON_ASSIGNTOPROJECT_NAME"]
    script_key = os.environ["SGDAEMON_ASSIGNTOPROJECT_KEY"]

    # Grab an sg connection for the validator.
    sg = shotgun_api3.Shotgun(server, script_name=script_name, api_key=script_key)

    # Bail if our validator fails.
    if not is_valid(sg, reg.logger):
        reg.logger.warning("Plugin is not valid, will not register callback.")
        return

    # Register our callback with the Shotgun_%s_Change event and tell the logger
    # about it.
    reg.registerCallback(
        script_name,
        script_key,
        chief_cmt,
        {"Shotgun_Note_Change":"user"}, #, ['user', 'is', {'type':'HumanUser', 'id':'yizeon' }]
        None,
    )
    reg.logger.debug("Registered callback.")


def is_valid(sg, logger):
    """
    Validate our args.
    :param sg: Shotgun API handle.
    :param logger: Logger instance.
    :returns: True if plugin is valid, None if not.
    """

    # Make sure we have a valid sg connection.
    try:
        sg.find_one("Note", [])
    except Exception, e:
        logger.warning(e)
        return

    return True


def sendMail(send, to, subject, content, imageurl):
    smtp = smtplib.SMTP_SSL('mail.azworks.co.kr', 465)
    smtp.login(send, '123456')
    msg = MIMEMultipart('alternative')
   
    msg['Subject'] = subject
    img = urllib2.urlopen(imageurl)
    imgfff = io.BytesIO(img.read())
     
    filename = img.info().get('content-disposition').split('=')[-1].replace('"','')
    content_type = img.info().maintype 
    imagef = MIMEImage(imgfff.read())
    imagef.add_header('Content-ID', '<image1>')
    imagef.add_header('Content-disposition', 'inline', filename=filename)
    imagef.add_header('Content-Type', content_type)
    imagef.add_header('Accept-Encoding', 'gzip')
    img.close()
    msg.attach(imagef)
    msg.attach(MIMEText(content, 'html', _charset="utf-8"))

    smtp.sendmail(send, to, msg.as_string())
    smtp.quit()
    
def userMail(user_id,sg):
    if(user_id==635):
        return
    user = sg.find_one("HumanUser", [["id", "is", user_id], ['sg_status_list', 'is', 'act']], ['email'])
    return str(user['email'])

def chief_cmt(sg, logger, event, args):
    
    meta = event.get("meta", {})
    
    if(meta['entity_type']=='Note'):
       
        note = sg.find_one("Note", [["id", "is", meta['entity_id']]], ['note_links','user','attachments', 'content', 'created_at'])
        
        if(str(note)=='None'):
            return
        
        if(note['user']['id']!=635):
            return
        
        if(str(note['attachments'])!='None' ):
            draw_image = ''
            for att in note['attachments']:
                attach = sg.find_one("Attachment", [["id", "is", att['id']]], ['this_file'])
                draw_image = "<img src ='"+str(attach['this_file']['url'])+"' style='max-width: 400px;' width='95%'> <br>" + draw_image
            
        
        
        for e in note['note_links']:
            
            if (e['type']=='Version' ):
                fields = ['project', 'entity','id', 'code', 'content','image','sg_uploaded_movie', 'sg_status_list', 'user', 'sg_path_to_movie','description', 'sg_task','sg_chiff_cmt', 'sg_leader_cmt', 'sg_cgi__cmt', 'sg_cmt', 'sg_dir_cmt', 'sg_pm_cmt']
                version = sg.find_one("Version", [["id", "is", e['id']], ['entity', 'is_not', None]], fields)
                
                rvlink=''
                imageurl = ''
                
                if (str(version)=='None'):
                    return
                
                if (str(version['image'])!='None'):
                    imageurl = str(version['image'])
                
                if(str(version['sg_path_to_movie'])!='None'):
                    rvlink = "rvlink://baked/"+str(version['sg_path_to_movie']).encode("hex")
                    
                uploaded_name=''
                if (str(version['sg_uploaded_movie'])!='None'):
                    uploaded_name = version['sg_uploaded_movie']['name']
                    
                notes = sg.find("Note", [["note_links", "is", {'type': 'Version', 'id':version['id']}], ['id', 'is_not', note['id']]], ['note_links','user','content','created_at'],[{'field_name': 'create_at', 'type': 'create_at', 'direction': 'desc'}])
                note_history = ''
                for x in notes:
                    if (str(x['content'])=='None'): 
                        x['content'] = '';
                    note_history = "<span style='color:#E06D42;'>[From-"+str(x['user']['name'])+"]["+str(x['created_at'])+"]</span> "+str(x['content'])+" <br>" + str(note_history)
                
                
                subject = '[Chief Cmt] ['+str(version['project']['name'])+'] '+str(version['entity']['type'])+' '+str(version['entity']['name'])+' / '+ str(version['sg_task']['name'])
                content = """<table width='95%' style='border-collapse: collapse; font-family: helvetica, arial, sans-serif; font-weight: 300; color: rgb(68, 68, 68); padding: 0px; margin: 0px auto; max-width: 1124px;' cellpadding='0' cellspacing='0' border='0' align='center'>
                    <tbody style=''>
                        <tr style=''>
                        <td style='vertical-align: top;'>
                            <table width='95%' border='0' cellspacing='0' cellpadding='0' style='padding: 0px;'>
                                <tbody style=''>
                                    <tr style=''>
                                        
                                        <td width='14px' style='background: rgb(65, 132, 243);'></td>
                                        <td style='padding: 40px 0px 20px; border-bottom: 2px solid rgb(49, 116, 169); background: rgb(65, 132, 243); color: rgb(255, 255, 255); font-size: 22px; font-weight: 600; font-family: roboto, arial, helvetica, sans-serif;'>
                                            Shotgun Version ::: Chief Comment<br style=''><div style='font-size: 11px;'>4thparty.shotgunstudio.com</div>
                                        </td>
                                        <td width='14px' style='background: rgb(65, 132, 243);'></td>
                                        
                                    </tr>
                                    <tr style=''>
                                        <td width='14px' style='background: rgb(65, 132, 243);'></td>
                                        <td style='background: rgb(255, 255, 255); border-top: 1px solid rgb(49, 100, 153); border-bottom: 1px solid rgb(255, 255, 255);'>&nbsp;</td>
                                        <td width='14px' style='background: rgb(65, 132, 243);'></td>
                                    </tr>
                                    <tr style=''>
                                        <td width='14px' style='background: rgb(250, 250, 250); border-left: 1px solid rgb(240, 240, 240); border-right: 1px solid rgb(240, 240, 240);'></td>
                                        <td style='background: rgb(255, 255, 255); padding: 0px 10px 20px; border-top: 1px solid rgb(255, 255, 255); border-bottom: 1px solid rgb(191, 191, 191);'>
                                            
                                            <table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style=''>
                                                <tbody style=''>
                                                    <tr style=''>
                                                        <td align='left' width='66%' style=''>
                                                            <div style='display: inline-block; background: rgb(213, 71, 62); color: rgb(255, 255, 255); font-weight: bold; font-size: 11px; padding: 2px;'></div>
                                                        </td>
                                                        <td rowspan='3' align='right' width='28%' valign='top' style=''>
                                                            <img pnsrc='cid:"""+str(version['image'])+"""' style='max-width: 230px;' width='95%' src='cid:image1'>
                                                        </td>
                                                    </tr>
                                                    <tr style=''>
                                                        <td align='left' style='padding: 10px 0px 5px; color: rgb(66, 133, 244); font-size: 21px; font-weight: 300; font-family: roboto, arial, helvetica, sans-serif;'>
                                                            ["""+str(version['project']['name'])+"""]  """+str(version['entity']['type'])+""" """+str(version['entity']['name'])+""" / """+ str(version['sg_task']['name'])+"""
                                                        </td>
                                                    </tr>
                                                    <tr style=''>
                                                        <td align='left' style='padding: 0px 0px 30px; color: rgb(68, 68, 68); font-size: 14px; font-weight: 300; font-family: roboto, arial, helvetica, sans-serif;'>
                                                            <font color='#999' style=''>Version Upload by</font> <b style=''>"""+str(version['user']['name'])+"""</b>
                                                        </td>
                                                    </tr>
                                                    
                                                    <tr style=''>
                                                        <td colspan='2' style='padding: 10px 0px; color: rgb(68, 68, 68); line-height: 24px; font-size: 14px; font-weight: 300; font-family: roboto, arial, helvetica, sans-serif;'>
                                                            <p style='margin: 0px; padding: 0px; word-break: break-all;'>
                                                            <b style=''>Artist Comment:</b><br style=''>"""+str(version['description'])+"""<br style=''><br style=''>"""+str(version['code'])+"""    <br style=''>                                                                                                                            
                                                        </p>
                                                        </td>
                                                    </tr>
                                                    
                                                    <tr style=''>
                                                        <td colspan='2' style='padding: 10px 0px; color: rgb(68, 68, 68); line-height: 24px; font-size: 14px; font-weight: 300; font-family: roboto, arial, helvetica, sans-serif;'>
                                                            <p style='margin: 0px; padding: 0px; word-break: break-all;'>
                                                            <b style='color:#E04296'>Chief Comment:</b>
                                                            <br style=''>"""+str(note['content'])+"""<br style=''><br style=''>[From-"""+str(note['user']['name'])+"""]["""+str(note['created_at'])+"""]<br style=''>
                                                            
                                                        </p>
                                                        </td>
                                                    </tr>
                                                    
                                                    <tr style=''>
                                                        <td colspan='2' style='padding: 10px 0px; color: rgb(68, 68, 68); line-height: 24px; font-size: 14px; font-weight: 300; font-family: roboto, arial, helvetica, sans-serif;'>
                                                            <p style='margin: 0px; padding: 0px; word-break: break-all;'>
                                                            <b style='color:#E06D42'>Others Comment:</b>
                                                                <br style=''>"""+note_history+"""<br style=''>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                    
                                                    <tr style=''>
                                                        <td colspan='2' style='padding: 10px 0px; color: rgb(68, 68, 68); line-height: 24px; font-size: 14px; font-weight: 300; font-family: roboto, arial, helvetica, sans-serif;'>
                                                            <b style=''>Version Files:</b><br style=''>
                                                            <p style='margin: 0px; padding: 0px 0px 10px; word-break: break-all;'>"""+str(version['sg_path_to_movie'])+"""</p>
                                                        </td>
                                                    </tr>
                        
                                                    <tr style=''>
                                                        <td colspan='2' style='padding: 10px 0px; color: rgb(68, 68, 68); line-height: 24px; font-size: 14px; font-weight: 300; font-family: roboto, arial, helvetica, sans-serif;'>
                                                            <b style=''>Version:</b><br style=''>
                                                            <p style='padding: 0px; margin: 0px; word-break: break-all;'>"""+uploaded_name+""" : <br style=''><span class='Object' role='link' id='OBJ_PREFIX_DWT88_com_zimbra_url'>
                                                            <a target='_blank' href='https://4thparty.shotgunstudio.com/page/media_center?type=Version&id="""+str(version['id'])+"""&global=true&project_sel=all'>https://4thparty.shotgunstudio.com/page/media_center?type=Version&id="""+str(version['id'])+"""&global=true&project_sel=all</a></span></p><br style=''>
                                                            <a href='"""+str(rvlink)+"""' style='background: rgb(66, 133, 244); padding: 3px 4px; color: rgb(255, 255, 255); text-decoration: none; font-weight: bold; font-size: 12px;' target='_blank'>play rv</a>
                                                            <hr style='display: block; height: 1px; border-width: 1px 0px 0px; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image: initial; border-top-style: solid; border-top-color: rgb(238, 238, 238); margin: 14px 0px; padding: 0px;'>
                                                        </td>
                                                    </tr>
                    
                                                </tbody>
                                            </table>
                                            
                                        </td>
                                        <td width='14px' style='background: rgb(250, 250, 250); border-left: 1px solid rgb(240, 240, 240); border-right: 1px solid rgb(240, 240, 240);'></td>
                                    </tr>
                                    <tr style=''>
                                        
                                        <td width='14px' style='background: rgb(250, 250, 250); border-left: 1px solid rgb(240, 240, 240); border-bottom: 1px solid rgb(240, 240, 240);'></td>
                                        <td style='padding: 20px 10px 60px; background: rgb(250, 250, 250); font-size: 9px; color: rgb(102, 102, 102); border-top: 2px solid rgb(223, 223, 223); border-bottom: 1px solid rgb(240, 240, 240);'>
                                            This email can't receive replies. This message is only received when an publish event occurs on the task that you are involved.
                                            <br style=''><br style=''>
                                             4th Creative Party Co., Ltd. 6 Centum 7-ro, Haeundae-gu, Busan, KOREA</td>
                                        <td width='14px' style='background: rgb(250, 250, 250); border-right: 1px solid rgb(240, 240, 240); border-bottom: 1px solid rgb(240, 240, 240);'></td>
                                        
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>"""
        
        
                
                emails = []
                emails.append('ejung@email.4thparty.co.kr')
                # cgi sup, sup, pm, tm
                pr = sg.find_one("Project", [["id", "is", version['project']['id']]], ["sg_vfx_supervisor", "sg_cg_supervisor", "sg_project_manager_2",'sg_sg_project_coordinator'])
                
                for att in pr['sg_vfx_supervisor']:
                    mail = userMail(att['id'], sg)
                    if(mail!=None and mail !=''):
                        emails.append(userMail(att['id'], sg))
                    
                for att2 in pr['sg_cg_supervisor']:
                    mail = userMail(att2['id'], sg)
                    if(mail!=None and mail !=''):
                        emails.append(userMail(att2['id'], sg))
                    
                for att3 in pr['sg_project_manager_2']:
                    mail = userMail(att3['id'], sg)
                    if(mail!=None and mail !=''):
                        emails.append(userMail(att3['id'], sg))
                    
                for att4 in pr['sg_sg_project_coordinator']:
                    mail = userMail(att4['id'], sg)
                    if(mail!=None and mail !=''):
                        emails.append(userMail(att4['id'], sg))
                
                sendMail('wave@azworks.co.kr', emails, subject, content, imageurl)
        


