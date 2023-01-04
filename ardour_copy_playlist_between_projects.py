# Created by Ben 
# Out of Order Enlgish Podcast: https://www.youtube.com/channel/UCiTiHX54WjoJok-PDgHVjBw
# Extraordinary English Podcast: https://www.youtube.com/channel/UC4_xy_GL4LZgM7a4ey2LCqw

import os           
import sys
import time
import xml.etree.ElementTree as ET

class ardour_project_op():


    def __init__(self) -> None:
        self.dst_max_source_id = 0
        self.src_medias = []
        self.media_ids_in_regions = []


    def copy_playlist_between_projects(self, path_src_project, path_dst_project):

        self.src_tree = ET.parse(path_src_project) 
        self.src_root = self.src_tree.getroot()

        self.dst_tree = ET.parse(path_dst_project)
        self.dst_root = self.dst_tree.getroot()

        self.get_max_source_id_from_destination()

        #print(root)
        # printing the attributes of the# first tag from the parent
        #print(root[0].attrib)
        
        # printing the text contained within first subtag of the 5th tag from the parent
        #print(root[5][0].text)

        print("PLAYLISTS from Source project")
        self.list_playlists_from_source_project()
        print("---")
        print("")
        wanted_plid = input("Type the playlist id you want to copy: ")
        print("Selected playlist id: " + wanted_plid)


        #rs = root.find('UnusedPlaylists')
        rs = self.src_root.find('Playlists')
        # find the first 'item' object
        #for pl in rs:
        #    print(pl.get('name'))

        pls_src = rs.findall('Playlist')
        for pl in pls_src:
            # if we don't need to know the name of the attribute(s), get the dict
            #print(pl.attrib)      
            # if we know the name of the attribute, access it directly
            #print(pl.get('name'))

            plname = pl.get("name")
            plid = pl.get("id")
            #2022-12 - If it's not the wanted playlist, ignore it
            if (plid != wanted_plid): 
                continue

            for rgn in pl.findall("Region"):
                #print(rgn.attrib)
                ch = rgn.get("channels")
                src_0 = int(rgn.get("source-0"))
                if src_0 not in self.media_ids_in_regions:
                    self.media_ids_in_regions.append(src_0)
                
                if (ch == "2"):
                    src_1 = int(rgn.get("source-1"))
                    if src_1 not in self.media_ids_in_regions:
                        self.media_ids_in_regions.append(src_1)




        rs = self.src_root.find('Sources').findall("Source")
        for source in rs:
            #print(src.attrib)
            mid = int(source.get("id"))

            for gid in self.media_ids_in_regions:
                if (mid==gid):
                    if (gid <= self.dst_max_source_id):
                        id_new = self.get_next_source_id()
                        self.change_source_id(mid, id_new)
                        #print(src)
                    self.src_medias.append(source)


        import glob
        gpath = os.path.abspath(os.path.join(path_src_project, os.pardir))
        gpath = os.path.join(gpath, "interchange", "*","audiofiles")
        path_src_interchange_audio = glob.glob(gpath)[0]
        #/media/data/Belgelerim/PROJE/ENLEM ve BOYLAM/2022-12_EB-172/interchange/2022-12_EB-172/audiofiles
        
        #DESTINATION Ardour project...

        #add media sources from src project to the dst project
        el = self.dst_root.find("Sources")
        for ms in self.src_medias:
            org_path = ms.get("origin")
            if (org_path == ""):
                org_path = os.path.join(path_src_interchange_audio, ms.get("name"))
                ms.set("origin", org_path)
            el.append(ms)

        dst_pls = self.dst_root.find("Playlists")
        src_pls = self.src_root.find('Playlists').findall('Playlist')
        for pl in src_pls:
            plname = pl.get("name")
            plid = pl.get("id")
            if (plid == wanted_plid):
                # for dst_pl in dst_pls.findall("Playlist"):
                #     if (dst_pl.get("id") == wanted_plid):
                #         print("")
                #         print("DESTINATION project already has the same playlist id: " + plid + " - pl name: " + plname)
                        #exit()
                gnewplid = self.generate_new_playlist_id_for_destination()
                gnewname = "mb-import_" + plname
                pl.set("id", str(gnewplid))
                pl.set("name", gnewname)
                pl.set("orig-track-id", "0") #unassign track
                dst_pls.append(pl)
                print("new plid: " , gnewplid, " - new pl name: ", gnewname)
                print( plname + " playlist inserted into the destination project. You can switch to it in Ardour GUI. Track > Playlists > Advanced > Copy from..." )


        #rs = dst_root.find('Sources').findall("Source")
        # for it in rs:
        #     #print(src.attrib)
        #     mid = it.get("id")
        #     if (media_ids.count(mid)): #if there is the same id in the destination project...
        #         if (src_medias.count(it)): #if the same media / source element... no further action needed
        #             continue
        #         else: #confliction... need to set a new id
        #             set_a_new_id()
            

        #add src project path to dst project 
        #<Option name="audio-search-path" value="
        dst_opts = self.dst_root.find('Config').findall('Option')
        for opt in dst_opts:
            opt_name = opt.get("name")
            if (opt_name == "audio-search-path"):
                opt_value = str(opt.get("value"))     
                gstr = ":" + os.path.abspath(os.path.join(path_src_project, os.pardir))
                if (opt_value.find(gstr) < 0):
                    opt_value += gstr
                   # opt.set("value", opt_value) #2022-12 - disable adding extra path

        #set new max id to dst project
        self.dst_root.set("id-counter", str(self.dst_max_source_id))


        #tree.write("/tmp/test2.xml")
        #tree.write("/tmp/test2.xml", xml_declaration=True) 
        #tree.write("/tmp/test2.xml", encoding='UTF-8', xml_declaration=True) 
        os.rename(path_dst_project, path_dst_project + "_" + str(int(time.time())) + ".bak")
        self.dst_tree.write(path_dst_project, encoding='UTF-8', xml_declaration=True)


        exit()

        # Converting the xml data to byte object, for allowing flushing data to file stream
        b_xml = ET.tostring(root) 
        # Opening a file under the name `items2.xml`, with operation mode `wb` (write + binary)
        with open("/tmp/test.xml", "wb") as f:
            f.write(b_xml)


    def list_playlists_from_source_project(self):
        src_pls = self.src_root.find('Playlists').findall('Playlist')
        for pl in src_pls:
            print(pl.get("id") + " : " + pl.get("name"))

    def get_max_source_id_from_destination(self):
        self.dst_max_source_id = int(self.dst_root.get("id-counter"))
        return

        rs = self.dst_root.find('Sources').findall("Source")
        for it in rs:
            sid = int(it.get("id"))
            self.dst_max_source_id = max(self.dst_max_source_id, sid)

    def generate_new_playlist_id_for_destination(self):
        gidmax = 0
        dst_pls = self.dst_root.find('Playlists').findall('Playlist')
        for pl in dst_pls:
            #print(pl.get("id") + " : " + pl.get("name"))
            gid = int(pl.get("id"))
            gidmax = max(gidmax, gid)
        
        return gidmax + 1

            
    def get_next_source_id(self):
        self.dst_max_source_id += 1
        return self.dst_max_source_id

    def change_source_id(self, pid_old, pid_new):
        #change it from Session/Sources/Source
        rs = self.src_root.find('Sources').findall("Source")
        for src in rs:
            #print(src.attrib)
            gid = int(src.get("id"))
            if (gid==pid_old):
                src.set("id", str(pid_new))
        
        #change it from Session/Playlists/Playlist/Region
        pls = self.src_root.find('Playlists').findall('Playlist')
        for pl in pls:
            for rgn in pl.findall("Region"):
                #print(rgn.attrib)
                ch = rgn.get("channels")
                src_0 = int(rgn.get("source-0"))
                if (src_0 == pid_old):
                    rgn.set("source-0", str(pid_new))
                    rgn.set("master-source-0", str(pid_new))
                
                if (ch == "2"):
                    src_1 = int(rgn.get("source-1"))
                    if (src_1 == pid_old):
                        rgn.set("source-1", str(pid_new))
                        rgn.set("master-source-1", str(pid_new))







try:
    if len(sys.argv) < 3:
       print("USAGE: " + sys.argv[0] + " [source_ardour_project] [destination_ardour_project]")
       sys.exit(0)

    args = sys.argv
    print(args)

    gsrc = args[1]
    gdst = args[2]
    #print("SRC: ", gsrc)
    #print("DST: ", gdst)
    #gsrc = "/media/data/Belgelerim/PROJE/O3EP/O3EP-5/O3EP-5.ardour"
    #gdst = "/media/data/Belgelerim/PROJE/O3EP/O3EP-5/O3EP-5.ardour"

    myproject = ardour_project_op()
    myproject.copy_playlist_between_projects(gsrc, gdst)

except Exception as ex:
    print (ex)


