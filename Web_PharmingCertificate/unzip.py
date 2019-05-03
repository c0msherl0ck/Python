import os
import zipfile
# unzipCertSet
def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        print(full_filename)
        filename = filename.replace(".zip","")
        print(filename)
        # make a directory by ip
        try:
            if not (os.path.isdir("unzipCertSet/"+filename)):
                os.makedirs(os.path.join("unzipCertSet/"+filename))
        except OSError:
            print("Failed to create directory!!")
        # extract .zip file to the directory
        zip = zipfile.ZipFile(full_filename)
        zip.extractall("unzipCertSet/"+filename+"/")
    return len(os.listdir(dirname))

cnt = search("certificate_set")
print(cnt)