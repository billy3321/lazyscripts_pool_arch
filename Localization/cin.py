#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2007 朱昱任 (Yuren Ju) <yurenju -AT- gmail.com>
# Copyright (C) 2007 洪任諭(PCMan) <pcman.tw -AT- gmail.com>
# Copyright (C) 2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 19 Dec 2008
# Install and config input method for one or more users.
# Released under GNU General Public License
#
# @name_enUS '' 
# @name_zhTW '安裝/設定 繁體中文輸入法'
# @desc_enUS ''
# @desc_zhTW '讓你安裝你想要的中文輸入法，有 scim, gcin 可選擇。令也支援在gcin中添加無蝦米輸入法。'
# @category 'Localization'
# @maintaner '2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>'
# @author '2007 洪任諭(PCMan) <pcman.tw -AT- gmail.com>'
# @author '2007 朱昱任 (Yuren Ju) <yurenju -AT- gmail.com>'
# @license 'GPL'
# @fedora
# @platform 'i386 amd64'
# @child 'noseeing-inst'

#import subprocess
import os
from string import Template
import pygtk
pygtk.require('2.0')
import gtk 
import commands

def apply_im_setting(user_name,selected_cin,target="users"):
      ims_cmd = "export INPUT_METHOD=\"%s\"" % (selected_cin)
      if target == "users":
          print "套用輸入法設定到" + user_name + "..."
          user_homedir=commands.getoutput('cat /etc/passwd | grep %s | cut -d ":" -f 6' % (user_name)).split('\n')
      
          user_profile_path = str(user_homedir[0])+'/.profile'
      elif target == "all":
          user_profile_path = "/etc/sysconfig/language"
      
      replace_cmd = "sed -i '/^export INPUT_METHOD=/d' %s" % (user_profile_path)
      os.system(replace_cmd)
      
      add_cmd = "echo '%s' >> %s" % (ims_cmd, user_profile_path)
      os.system(add_cmd)
      
    
    
def noseeing_yes_no():
    msg="請問您是否要安裝無蝦米輸入法？"
    dlg = gtk.MessageDialog \
            (None, gtk.DIALOG_MODAL, \
            gtk.MESSAGE_QUESTION, \
            gtk.BUTTONS_YES_NO, msg)

    ret = dlg.run ()
    dlg.destroy ()
    if ret == gtk.RESPONSE_YES:
     os.system( 'scripts/noseeing-inst' )

def sel_users(selected_cin):
    USERS_LIST=commands.getoutput('cat /etc/passwd | grep bash | cut -d ":" -f 1').split('\n')
    USERS_LIST.pop(0)

    dlg_bts={}
    dlg = gtk.MessageDialog \
        (None, gtk.DIALOG_MODAL,  \
        gtk.MESSAGE_QUESTION, \
        gtk.BUTTONS_OK)
    dlg.set_markup ('<b>請選擇您的輸入法設定要套用的使用者細項：</b>')
    for user_name in USERS_LIST:
     user_name_box= user_name + "_box"
     dlg_bts[user_name_box]=gtk.CheckButton(user_name)
     dlg.vbox.pack_start(dlg_bts[user_name_box],True,True,2)

    dlg.vbox.show_all ()

    ret = dlg.run ()
    for user_name in USERS_LIST:
     user_name_box= user_name + "_box"
     if dlg_bts[user_name_box].get_active():
         apply_im_setting(user_name, selected_cin,users)

      #user_profile = open(str(user_homedir[0])+'/.profile', 'w')
      #profile_contain = user_profile.readlines()
      
      #profile_len = len(profile_contain)
      #search_str = re.compile('^export INPUT_METHOD=')
      #for i in range(profile_len):
      # if search_str.match(profile_contain[i]):
      #  del profile_contain[i]
      #user_profile.write(ims_cmd)
      #user_profile.close()
      #os.system(ims_cmd)



def user_scope (selected_cin):
    dlg = gtk.MessageDialog \
        (None, gtk.DIALOG_MODAL,  \
        gtk.MESSAGE_QUESTION, \
        gtk.BUTTONS_OK)
    dlg.set_markup ('<b>請選擇您的輸入法設定要套用的使用者範圍：</b>')
 
    currectuser_btn=gtk.RadioButton (None, '只套用到我自己')
    dlg.vbox.pack_start (currectuser_btn, False, True, 2)
    alluser_btn =gtk.RadioButton (currectuser_btn ,'套用到所有使用者')
    dlg.vbox.pack_start (alluser_btn, False, True, 2)
    seluser_btn =gtk.RadioButton (currectuser_btn ,'選擇套用的使用者')
    dlg.vbox.pack_start (seluser_btn, False, True, 2)

    dlg.vbox.show_all ()

    ret = dlg.run ()
    currectuser = currectuser_btn.get_active()
    alluser = alluser_btn.get_active()
    seluser = seluser_btn.get_active()

    dlg.destroy ()
    if ret != gtk.RESPONSE_OK:
       return False
    while gtk.events_pending ():
      gtk.main_iteration ()

    if currectuser:
       print "套用輸入法設定到當前使用者..."
       #ims_cmd = "su -c \"im-switch -s %s\" %s" % (selected_cin, os.environ['REAL_USER']) 
       #os.system(ims_cmd)
       user_name = os.environ['REAL_USER']
       apply_im_setting(user_name, selected_cin,users)
       

    elif alluser:
       print "套用輸入法設定到所有使用者..."
    #   ims_cmd = "sudo im-switch -s %s" % (selected_cin)
    #   os.system(ims_cmd)
       apply_im_setting(none, selected_cin,"all")
    elif seluser:
       sel_users(selected_cin)


def main():
    yum_cmd = "yum -y install "
    xhost_cmd = "xhost local:%s" % (os.environ['REAL_USER'])
    print xhost_cmd
    os.system(xhost_cmd)
    gcin_text = "gcin \"由台灣網友開發的輸入法，有許多在地化的調校，\n是在臺灣相當受到歡迎的中文輸入法。\n有許多方便的功能，穩定而強大，內建多種輸入法，\n包括功能類似微軟新注音的詞音輸入法、並「可支援無蝦米」。\n但和 Windows 下常見的操作習慣相差不少，新手可能會很不習慣。\n\""
    scim_text = "scim \"Ubuntu 預設的中文輸入法，可以輸入多國文字，功能強大，\n操作和 Windows 上接近，內含類似新注音，相當知名的新酷音輸入法，\n但是比較龐大，目前穩定性也不及 gcin\n\""
    dialog_text = "--text=下列是最常見的二種中文輸入法，'請選擇您喜好的輸入法，\n若您無法決擇，建議可以考慮 gcin：\n'"
    zenity_cmd = Template("zenity --width=512 --height=480 --list --title='選擇輸入法' --column='名稱' --column='敘述' $dialog_text $gcin $scim").substitute(gcin=gcin_text, scim=scim_text, dialog_text=dialog_text)
    print zenity_cmd
    fin, fout = os.popen2(zenity_cmd)
    selected_cin = fout.read().strip()

    #os.system(apt_cmd + "im-switch")

    if selected_cin == 'gcin' or selected_cin == 'scim':
        os.system(yum_cmd + selected_cin)

        if selected_cin == "scim":
            os.system(yum_cmd + "scim-qtimm scim-chewing")
        elif selected_cin == 'gcin':
            os.system("zypper ar http://download.opensuse.org/repositories/home:/swyear/openSUSE_11.1/ swyear")
            os.system(yum_cmd +'gcin-qt3-immodule' )
            # install noseeing
            # FIXME: 使用者應該可以選擇不要安裝無蝦米
            #os.system( 'scripts/noseeing-inst' )
            noseeing_yes_no()

        user_scope(selected_cin)

        #ims_cmd = "su -c \"im-switch -s %s\" %s" % (selected_cin, os.environ['REAL_USER']) 
        #os.system(ims_cmd)

if __name__ == '__main__':
    main()
