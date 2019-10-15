import face_recognition



class Face_check():

    #人脸对比
    def check_face(known_face_encoding, unknown_picture):
        unknown_picture2 = face_recognition.load_image_file(unknown_picture)
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture2)[0]

        # 距离值  越低越是，越大越不是同一个人

        match_results= face_recognition.compare_faces( [known_face_encoding], unknown_face_encoding)
        return  match_results

    #编码图片
    def register_encoding_face(face):

        #加载图片
        picture=face_recognition.load_image_file(face)
        #编码
        face_encoding=face_recognition.face_encodings(picture)[0]
        return face_encoding






