# Application to support face-recognition in military areas

## Tên thành viên
Group: Làm sai cái đúng
1. 23020350 Nguyễn Đăng Dương
2. 23020354 Tôn Thành Đạt
3. 23020366 Nguyễn Trung Hiếu
4. 23020360 Trương Trọng Đức
5. 23020393 Muộn Quốc Khánh Linh
## Mô tả dự án
**1. Chủ đề:**  
Nhận diện gương mặt ở khu vực an ninh. Hiện nay, tại các cơ sở quân sự, công nghệ xác định khuôn mặt đóng góp không nhỏ trong việc kiểm soát truy cập vào các khu vực an ninh, chẳng hạn như các kho vũ khí và các khu vực tập luyện. Nhận thấy được điều đó, hệ thống nhận diện gương mặt, kiểm tra người được nhận diện có được phép vào khu vực quân sự này hay không đã được nhóm quyết định thực hiện.  
**2. Hệ thống**  
&nbsp;&nbsp;&nbsp;&nbsp;2.1. Phân tích use case diagram  
&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/user-attachments/assets/7955f453-c2f8-4f04-a755-df866534ecdb" alt="..." width="550"/>  
&nbsp;&nbsp;&nbsp;&nbsp;Nếu custumer là user thì sẽ có 1 use case là nhận diện gương mặt.  
&nbsp;&nbsp;&nbsp;&nbsp;Nếu customer là admin thì sẽ có 3 use case là thêm người dùng, chỉnh sửa thông tin người dùng, xoá người dùng khỏi database.  
&nbsp;&nbsp;&nbsp;&nbsp;2.2. Sequence diagram  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.1. User sequence diagram  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/user-attachments/assets/7f5f5d62-1a9c-4032-acf9-800587e51223" alt="..." width="550"/>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.2. Admin sequence diagram  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/user-attachments/assets/0f22fab3-570a-428c-8632-c1adde22934f" alt="..." width="550"/>  
&nbsp;&nbsp;&nbsp;&nbsp;2.3. Phân tích class diagram  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/user-attachments/assets/20a891bb-5cc9-4f04-874d-8d539327cb52" alt="..." width="950"/>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Tổng quan về class diagram**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sơ đồ lớp bao gồm 7 lớp chính: ImageData, WebService, ModelService, AppService, DBUtils, ModelUtils, và SupabaseClient. Các lớp này đại diện cho các thành phần cốt lõi của hệ thống nhận diện khuôn mặt, xử lý hình ảnh, phát hiện khuôn mặt, tạo embedding, tương tác cơ sở dữ liệu, và dịch vụ API. Mối quan hệ giữa các lớp được biểu thị bằng các mũi tên có nhãn, chỉ ra các phụ thuộc (ví dụ: "uses", "uses methods", "uses for DB").  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a. ImageData  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Attributes: image_data: str (public). Purpose: Dữ liệu ảnh được mã hoá dưới dạng base64, làm đầu vào cho endpoit API nhận diện khuôn mặt. Source: Trong web_service.py.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b. WebService  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Attributes: app: FastAPI (public). Methods: encode_image_to_base64(image) và predict(data: ImageData) Purpose: API cung cấp các điểm cuối cho nhận diện khuôn mặt. Xử lý hình ảnh đầu vào (qua ImageData) và sử dụng ModelService để phát hiện khuôn mặt và so sánh embedding. Source: Trong web_service.py.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c. ModelService  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Attributes: backend_db_url: str (public). Methods: ensure_facenet_model(), detect_face(frame), get_face_embedding(face_img), load_saved_embeddings(), compare_embedding(embedding, saved_data, threshold). Purpose: Xử lý logic nhận diện khuôn mặt cốt lõi, bao gồm khởi tạo mô hình, truy cập camera, phát hiện khuôn mặt, tạo embedding, và so sánh với các embedding đã lưu. Source: Trong model_service.py.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d. AppService  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Attributes: app: FastAPI (public), logger: Logger (private). Methods: upload_image_to_supabase(image_bytes, file_name), add_person(name, image, chuc_vu), get_embeddings(), get_people(), delete_person(person_id), update_person(person_id, name, image, chuc_vu). Purpose: Xử lý các thao tác CRUD (tạo, đọc, cập nhật, xóa) cho bản ghi người dùng, bao gồm lưu trữ hình ảnh và embedding trên Supabase. Source: Trong app.py.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;e. DBUtils    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Methods: save_embedding(name, embedding, image_url, chuc_vu). Purpose: Lưu embedding và dữ liệu người dùng vào cơ sở dữ liệu Supabase. Source: Trong db_utils.py.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;f. ModelUtils     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Methods: ensure_facenet_model(), detect_face(frame), get_embedding(image_bytes). Purpose: Phát hiện khuôn mặt và tạo embedding, được AppService sử dụng để xử lý hình ảnh người dùng trong các thao tác CRUD. Source: Trong model_utils.py.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;g. SupabaseClient       
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Attributes: SUPABASE_URL: str, SUPABASE_KEY: str, supabase: Client. Purpose: Quản lý kết nối với cơ sở dữ liệu Supabase, cung cấp instance client được sử dụng cho các thao tác cơ sở dữ liệu. Source: Trong supabase_client.py.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Mối quan hệ**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	WebService → ImageData ("uses"): WebService sử dụng ImageData làm cấu trúc dữ liệu đầu vào cho phương thức predict, nhận hình ảnh được mã hóa base64.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	WebService → ModelService ("uses methods"): WebService phụ thuộc vào ModelService cho các tác vụ nhận diện khuôn mặt, gọi các phương thức như detect_face, get_face_embedding, và compare_embedding để xử lý hình ảnh và nhận diện người dùng.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	ModelService → SupabaseClient ("uses for load_saved_embeddings"): ModelService sử dụng SupabaseClient để lấy các embedding đã lưu từ cơ sở dữ liệu thông qua phương thức load_saved_embeddings.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	AppService → ModelUtils ("uses get_embedding"): AppService sử dụng ModelUtils để tạo embedding cho hình ảnh người dùng mới trong các thao tác add_person và update_person.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	AppService → DBUtils ("uses save_embedding"): AppService dựa vào DBUtils để lưu embedding và thông tin người dùng vào cơ sở dữ liệu khi thêm người dùng.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	AppService → SupabaseClient ("uses for DB"): AppService sử dụng SupabaseClient cho các thao tác cơ sở dữ liệu như lấy embedding (get_embeddings) và quản lý bản ghi người dùng (get_people, delete_person).  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	DBUtils → SupabaseClient ("uses for DB"): DBUtils sử dụng SupabaseClient để thực hiện lưu embedding thông qua phương thức save_embedding.  
&nbsp;&nbsp;&nbsp;&nbsp;2.4. Cách sử dụng (usage)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Để nhận diện gương mặt, click chọn mở camera, nếu được vào hệ thống AI trả về kết quả tên, chức vụ và trạng thái được vào; nếu không được vào, hệ thống trả về Unknown, và trạng thái không được vào. Để tắt camera, click chọn tắt camera.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Đối với admin, để thêm người dùng, click chọn vào nút thêm người dùng góc trái, điền thông tin rồi chọn lưu. Để sửa, và xoá thì chọn ở cột phía bên phải. Sau khi sửa xong, click chọn lưu.
## Liên kết docker hub
### Bước 1: Xây dựng và gắn thẻ hình ảnh Docker:
```bash
docker tag AIsystemproject-frontend tonthanhdat/csai-frontend
docker tag AIsystemproject-backend_database tonthanhdat/csai-backend_database
docker tag AIsystemproject-backend_ai tonthanhdat/csai-backend_ai
```
### Bước 2: Đẩy lên Docker Hub:
``` bash
docker login
docker push tonthanhdat/csai-frontend
docker push tonthanhdat/csai-backend_database
docker push tonthanhdat/csai-backend_ai
```
 
Toàn bộ các image đã được đẩy lên Docker Hub với tên người dùng `tonthanhdat`. Bạn có thể pull trực tiếp chúng bằng các liên kết dưới đây:

| Thành phần        | Docker Hub Link |
|-------------------|------------------|
| Backend AI        | [tonthanhdat/csai-backend_ai](https://hub.docker.com/r/tonthanhdat/csai-backend_ai) |
| Backend Database  | [tonthanhdat/csai-backend_database](https://hub.docker.com/r/tonthanhdat/csai-backend_database) |
| Frontend          | [tonthanhdat/csai-frontend](https://hub.docker.com/r/tonthanhdat/csai-frontend) |

---
## Cách Chạy Hệ Thống

### Bước 1: Lưu tệp docker-compose.yml được cung cấp

### Bước 2: Khởi chạy hệ thống
``` bash 
docker-compose up -d
```
### Bước 3: Truy cập ứng dụng tại
####  http://localhost:8080

## Project status
The project is completed
## Notes
The application is writtened for face-recognition purposes.
