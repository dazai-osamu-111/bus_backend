import googlemaps
import pymysql
from datetime import datetime

# Cấu hình Google Maps API
API_KEY = 'AIzaSyAnI_7dbzhe2FS7kr1lXvqXId2AIBvUXB8'
gmaps = googlemaps.Client(key=API_KEY)

# Cấu hình kết nối MySQL
db_config = {
    'user': 'root',
    'password': 'uxg',
    'host': 'localhost',
    'database': 'busrouting'
}

# Danh sách địa điểm

# xe 01
# locations = [
#     "BX Gia Lâm", "549 Nguyễn Văn Cừ", "Trường THPT Nguyễn Gia Thiều", 
#     "E3.1 Điểm trung chuyển Long Biên", "50 Hàng Cót", "28 Đường Thành", 
#     "Bệnh viện Phụ sản TW", "Bệnh viện Phụ sản Trung ương", 
#     "Tổng Công Ty Đường Sắt Việt Nam - 116 Lê Duẩn", "Ga Hà Nội", "78-80A Khâm Thiên", 
#     "274-276 Khâm Thiên", "142-144 Nguyễn Lương Bằng", "Gò Đống Đa", 
#     "290 Tây Sơn", "Số 108 Nguyễn Trãi", "Chợ Thượng Đình", 
#     "Trường Đại học Khoa học Tự nhiên, Đại học Quốc gia Hà Nội", "Cục Sở hữu trí tuệ", "Bách hóa Thanh Xuân", 
#     "Đại Học Hà Nội", "Công Ty Cp Xây Dựng Công Trình Giao Thông 873", "Học viện An Ninh nhân dân", 
#     "Học viện Bưu chính viễn thông", "Big C Hà Đông - Hồ Gươm Plaza", 
#     "Sở Tư pháp Hà Nội - Cầu Trắng Hà Đông", "Bưu điện Hà Đông", 
#     "80 Quang Trung", "Nhà thi đấu Hà Đông", "350 - 352 Quang Trung", 
#     "Giữa số 428 - 430 Quang Trung", "530 - 532 Quang Trung", 
#     "678 - 680 Quang Trung", "Nissan Hà Đông", "Đối diện Trường TH Kinh tế Hà Tây", 
#     "BX Yên Nghĩa"
# ]

# locations = [
#     "BX Yên Nghĩa",
#     "Trường Trung Cấp Kinh Tế - Tài Chính Hà Nội",
#     "Đối diện Nissan Hà Đông",
#     "807 Quang Trung",
#     "707-709 Quang Trung, Hà Đông",
#     "Ngã tư Quang Trung, Lê Trọng Tấn - Nhà ga La Khê",
#     "Chợ La Khê",
#     "Công Ty Cplh Thực Phẩm - 267 Quang Trung - Hà Đông",
#     "Bệnh viện Đa khoa Hà Đông",
#     "Bưu điện Hà Đông",
#     "Sở Tư Pháp Hà Nội",
#     "Ga Văn Quán",
#     "Siêu thị Nguyễn Kim - Km10 Nguyễn Trãi (Hà Đông)",
#     "Đại học Kiến trúc Hà Nội",
#     "Học viện An Ninh nhân dân",
#     "Ga Phùng Khoang",
#     "517 Nguyễn Trãi",
#     "Tổng Công ty xây dựng Sông Đà - 493 Nguyễn Trãi",
#     "Học viện Khoa học Xã hội",
#     "Công ty Giày Thượng Đình",
#     "Trường ĐH Khoa học tự nhiên",
#     "Ga Thượng Đình",
#     "129T Nguyễn Trãi",
#     "Trường Đại học Thuỷ Lợi",
#     "Đại Học Công Đoàn - 169 Tây Sơn",
#     "83 Nguyễn Lương Bằng",
#     "221A-221B Khâm Thiên",
#     "Đài tưởng niệm Khâm Thiên",
#     "Cung VH Hữu Nghị Việt Xô",
#     "65 Quán Sứ",
#     "Bệnh viện Việt Đức",
#     "115 Phùng Hưng",
#     "Đối diện 16 Phùng Hưng",
#     "Ô Quan Chưởng",
#     "Tổng cục Hải Quan - 162 Nguyễn Văn Cừ (cột trước)",
#     "358 Nguyễn Văn Cừ",
#     "Đối diện 447 Ngọc Lâm",
#     "BX Gia Lâm"
# ]


# locations = [
#     "Bãi Đỗ Xe Buýt Trần Khánh Dư",
#     "Trạm Trung Chuyển Xe Buýt Trần Khánh Dư (Khu Đón Khách)",
#     "Đối diện Bệnh Viện Trung ương Quân đội 108 - Trần Hưng Đạo",
#     "Đại học Khoa học tự nhiên",
#     "Hè cạnh vườn hoa 19-8, đường Hai Bà Trưng",
#     "Trung tâm thương mại Tràng Tiền Plaza",
#     "Bệnh viện Hữu Nghị Việt Nam - Cu Ba",
#     "6-8 Tràng Thi",
#     "Bệnh viện Việt Đức",
#     "Cửa Nam - Phố ẩm thực Tống Duy Tân",
#     "Vườn hoa Lênin - Cột Cờ Hà Nội",
#     "Bệnh viện Xanh Pôn",
#     "Văn Miếu Quốc Tử Giám",
#     "Nhà Thờ Hàng Bột",
#     "Ngã 5 Ô Chợ Dừa",
#     "142-144 Nguyễn Lương Bằng",
#     "Gò Đống Đa",
#     "290 Tây Sơn",
#     "Số 108 Nguyễn Trãi",
#     "Chợ Thượng Đình",
#     "322 Nguyễn Trãi",
#     "Cục Sở hữu trí tuệ",
#     "Bách hóa Thanh Xuân",
#     "Đại Học Hà Nội",
#     "Công Ty Cp Xây Dựng Công Trình Giao Thông 873",
#     "Học viện An Ninh nhân dân",
#     "Học viện Bưu chính viễn thông",
#     "Big C Hà Đông - Hồ Gươm Plaza",
#     "Sở Tư pháp Hà Nội - Cầu Trắng Hà Đông",
#     "Bưu điện Hà Đông",
#     "80 Quang Trung",
#     "Nhà thi đấu Hà Đông",
#     "350 - 352 Quang Trung",
#     "Giữa số 428 - 430 Quang Trung",
#     "530 - 532 Quang Trung",
#     "678 - 680 Quang Trung",
#     "Nissan Hà Đông",
#     "Đối diện Trường TH Kinh tế Hà Tây",
#     "BX Yên Nghĩa"
# ]

# locations = [
#     "BX Yên Nghĩa",
#     "Trường Trung Cấp Kinh Tế - Tài Chính Hà Nội",
#     "Đối diện Nissan Hà Đông",
#     "807 Quang Trung",
#     "707-709 Quang Trung, Hà Đông",
#     "Ngã tư Quang Trung, Lê Trọng Tấn - Nhà ga La Khê",
#     "Chợ La Khê",
#     "Công Ty Cplh Thực Phẩm - 267 Quang Trung - Hà Đông",
#     "Bệnh viện Đa khoa Hà Đông",
#     "Bưu điện Hà Đông",
#     "Sở Tư Pháp Hà Nội",
#     "Ga Văn Quán",
#     "Siêu thị Nguyễn Kim - Km10 Nguyễn Trãi (Hà Đông)",
#     "Đại học Kiến trúc Hà Nội",
#     "Học viện An Ninh nhân dân",
#     "Ga Phùng Khoang",
#     "517 Nguyễn Trãi",
#     "Tổng Công ty xây dựng Sông Đà - 493 Nguyễn Trãi",
#     "Học viện Khoa học Xã hội",
#     "Công ty Giày Thượng Đình",
#     "Công ty thuốc là Thăng Long",
#     "Ga Thượng Đình",
#     "129T Nguyễn Trãi",
#     "Trường Đại học Thuỷ Lợi",
#     "Trường Đại Học Công Đoàn",
#     "83 Nguyễn Lương Bằng",
#     "UBND quận Đống Đa",
#     "Đài tưởng niệm Khâm Thiên",
#     "Văn Miếu Quốc Tử Giám",
#     "Nhà Thờ Hàng Bột",
#     "Vườn hoa Lênin - Cột Cờ Hà Nội",
#     "Bệnh viện Phụ sản trung ương",
#     "Trung tâm thương mại Tràng Tiền Plaza",
#     "16 Hai Bà Trưng",
#     "Nhà hát Lớn Hà Nội",
#     "Bãi Đỗ Xe Buýt Trần Khánh Dư"
# ]

# Tuyến 04
# locations = [
#     "Long Biên - Tuyến 04",
#     "E3.4 Điểm trung chuyển Long Biên",
#     "Ngã 4 Nguyễn Hữu Huân - Hàng Mắm",
#     "Cung thiếu Nhi Hà Nội",
#     "Đối diện Đại học Dược Hà Nội",
#     "34-36 Tăng Bạt Hổ",
#     "48B Tăng Bạt Hổ",
#     "172 Lò Đúc",
#     "86 Kim Ngưu",
#     "Tập thể E6 Quỳnh Mai",
#     "Cửa hàng nhựa đường số 3 - 344 Kim Ngưu",
#     "Đối diện 61 Tam Trinh",
#     "Đối diện 161 - 163 Tam Trinh",
#     "20 Lĩnh Nam",
#     "Đối diện 123 Lĩnh Nam",
#     "Đối diện số 271 Lĩnh Nam",
#     "Trường THPT Hoàng Văn Thụ",
#     "376-378 Lĩnh Nam",
#     "Bưu Điện Trung Tâm 6 - 582 Lĩnh Nam",
#     "Đình Nam Dư Hạ",
#     "Chùa Khuyến Lương",
#     "Số nhà 43 - Tổ 14 - Phường Yên Sở",
#     "Số nhà 30 Yên Sở, Phường Yên Sở",
#     "Đối diện Công Viên Yên Sở, Hoàng Mai",
#     "Qua lối rẽ khu hành chính quận Hoàng Mai",
#     "Số 2 Ngọc Hồi, đối diện tập thể bến xe Nước Ngầm",
#     "Qua đối diện công Ty Cổ Phần Điện Công Nghiệp Hà Nội 30m",
#     "Tòa nhà Nơ 3 - Trần Thủ Độ",
#     "Nhà No9 KĐT Pháp Vân",
#     "BV Nội Tiết TW cơ sở 2 - Tuyến 04"
# ]

# locations = [
#     "BV Nội Tiết TW cơ sở 2 - Tuyến 04",
#     "Đối diện nhà No9 KĐT Pháp Vân",
#     "Công viên khu đô thị Tứ Hiệp Pháp Vân (đối diện tòa nhà Nơ 3)",
#     "Công Ty Cổ Phần Điện Công Nghiệp Hà Nội",
#     "Bến xe Nước Ngầm",
#     "Công Viên Yên Sở, Hoàng Mai",
#     "Đường vào KĐT Gamuda",
#     "Qua đường vào khu tái định cư X2A 30m",
#     "Số nhà 15 - Tổ 15 - Phường Yên Sở",
#     "Trường mầm non Trần Phú - Hoàng Mai",
#     "Trước nhà máy nước Đông Dư",
#     "Ngõ 595 - Đối diện 602 Lĩnh Nam",
#     "Chợ Lòng Thuyền",
#     "Doanh Trại Quân Đội Nhân Dân - 393 Lĩnh Nam",
#     "239 Lĩnh Nam",
#     "Công ty CP Dệt CN Hà Nội",
#     "Đối diện 72 Lĩnh Nam",
#     "89 Nguyễn Tam Trinh",
#     "Đối diện 346 Kim Ngưu",
#     "Đối diện Tập thể E6 Quỳnh Mai",
#     "Đối diện Bãi trông giữ xe Công ty khai thác điểm đỗ xe Hà Nội tại 98 Kim Ngưu",
#     "131 Lò Đúc",
#     "77 Lò Đúc",
#     "61 Phan Chu Trinh",
#     "Nhà hát Lớn Hà Nội",
#     "Ngân hàng Nhà nước Việt Nam - Vườn hoa con Cóc",
#     "23 Hàng Tre - Ngã 4 Lò Sũ",
#     "Hàng Muối - Cầu Chương Dương",
#     "Điểm trung chuyển Long Biên (điểm E3.3)",
#     "Long Biên - Tuyến 04"
# ]

# Tuyến )5

# locations = [
#     "KĐT Linh Đàm",
#     "Nhà NƠ. 1A KĐT Linh Đàm",
#     "Đối Diện Trạm Cấp Nước Linh Đàm (Đối Diện Chung Cư HH1C) - Nguyễn Hữu Thọ",
#     "Công viên Bắc Linh Đàm",
#     "Cầu Dậu - Khu đô thị Bắc Linh Đàm",
#     "Đối diện cổng phụ Bệnh viện đa khoa y học cổ truyền",
#     "Trạm dừng Đối diện trường Tiểu học THCS Đại Kim",
#     "Đối diện 222 Kim Giang",
#     "Đối diện 32 Kim Giang",
#     "Đối diện 272 Khương Đình",
#     "Đối diện 134 Khương Đình",
#     "Chợ Thượng Đình",
#     "322 Nguyễn Trãi",
#     "90 Nguyễn Tuân",
#     "Làng Sinh viên Hacinco",
#     "Nhà N2C KĐT Trung Hòa Nhân Chính",
#     "Trường THPT chuyên Hà Nội",
#     "Trường THPT Nguyễn Bỉnh Khiêm - Đường Nguyễn Chánh",
#     "54 Mạc Thái Tông",
#     "Tòa nhà F15 - Trung Kính",
#     "Trước trường THCS Yên Hòa 30m",
#     "Qua Đối Diện Viện Huyết Học Và Truyền Máu Trung Ương 20M - Phạm Văn Bạch",
#     "Sân Bóng Đồng Bông - Tôn Thất Thuyết (Gần ĐH FPT)",
#     "Trường ĐH FPT",
#     "Cục Đăng Kiểm Việt Nam (Nguyễn Hoàng)",
#     "36 Nguyễn Hoàng",
#     "KĐT Phú Mỹ - Nguyễn Hoàng",
#     "Số 4 Hàm Nghi",
#     "202 Hồ Tùng Mậu",
#     "Đối diện 51 Đường K1 Cầu Diễn",
#     "Lối rẽ vào ga Phú Diễn",
#     "Đối diện cổng làng Phú Diễn",
#     "Điểm Đỗ Xe Buýt Phú Diễn (Trại Gà)"
# ]

# locations = [
#     "Điểm Đỗ Xe Buýt Phú Diễn (Trại Gà)",
#     "Cổng làng Phú Diễn",
#     "Đối diện Ga Phú Diễn",
#     "Cổng trường ĐH tài nguyên môi trường",
#     "Trụ sở Quận uỷ Nam Từ Liêm",
#     "Hè trước Đơn nguyên 2 KTX Mỹ Đình",
#     "103 Nguyễn Hoàng",
#     "29 Nguyễn Hoàng",
#     "Trước 100m ngã 4 Nguyễn Hoàng",
#     "Bộ Nội Vụ, Bộ Tài Nguyên Môi Trường",
#     "Ô D27 - Phạm Văn Bạch",
#     "Đối diện trường THCS Yên Hòa",
#     "Đại Học Phương Đông - 201B Trung Kinh",
#     "Cty CP Xây Lắp Bưu Điện - Đường Vũ Phạm Hàm",
#     "Đối Diện Trường THPT Nguyễn Bỉnh Khiêm - Đường Nguyễn Chánh",
#     "Đối diện Trường THPT chuyên Hà Nội",
#     "Đối diện Nhà N2A KĐT Trung Hòa Nhân Chính",
#     "Viện Khoa Học Hình Sự - 99 Nguyễn Tuân",
#     "Cục Sở hữu trí tuệ",
#     "Công ty Giày Thượng Đình",
#     "Trường ĐH Khoa học tự nhiên",
#     "Đối diện 81 - 83 Khương Đình",
#     "254 - 256 Khương Đình",
#     "42 Kim Giang",
#     "214 Kim Giang",
#     "292 Kim Giang",
#     "Cách cổng BV đa khoa y học cổ truyền 50m",
#     "Cầu Dậu - Khu đô thị Bắc Linh Đàm",
#     "Nhà HH2A khu đô thị Linh Đàm",
#     "KĐT Linh Đàm"
# ]

# Tuyến 07

# locations = [
#     "Cầu Giấy - Tuyến 07",
#     "Điểm trung chuyển Cầu Giấy - Thủ Lệ 01",
#     "Số 148-150 Cầu Giấy",
#     "Đối Diện Trường Cao Đẳng Điện Tử - Điện Lạnh Hà Nội",
#     "Bảo tàng Dân tộc học VN",
#     "90 Hoàng Quốc Việt",
#     "122-124 Hoàng Quốc Việt",
#     "212 Hoàng Quốc Việt",
#     "Trạm trung chuyển xe buýt Hoàng Quốc Việt (cột sau)",
#     "655 Phạm Văn Đồng",
#     "36A Phạm Văn Đồng",
#     "UBND phường Cổ Nhuế 1 - 601 Phạm Văn Đồng",
#     "527 Phạm Văn Đồng",
#     "Qua 70M Đường Vào Công Viên Hòa Bình - Phạm Văn Đồng",
#     "373 Phạm Văn Đồng",
#     "189 Phạm Văn Đồng",
#     "Qua ngã 3 Hải Bối",
#     "Qua ngã tư khu CN Thăng Long 100m",
#     "Đối diện UBND xã Kim Chung",
#     "Qua cầu chui dân sinh số 4 - đường vào thôn Nhuế, Km 11+200",
#     "Cầu Vân Trì",
#     "Trước 70m cầu vượt Ngã tư Nam Hồng Cao tốc BTL",
#     "Công ty cơ khí Nam Hồng",
#     "Đối diện KCN Quang Minh (Melinh Palaza)",
#     "Nhà Máy Tấm Lợp Vitmetal- Km 8+850 Cao Tốc Btl-Nb",
#     "Soát vé cao tốc Bắc Thăng Long",
#     "Ngã Tư Cao Tốc TL- Phúc Yên - Km 11+700 Cao Tốc BTL-NB",
#     "Qua 50m ngã 3 vào thôn Điền Xá",
#     "Đối diện nhà ga T2 sân bay Nội Bài",
#     "Đối diện nhà ga T1 sân bay Nội Bài",
#     "Nội Bài"
# ]

# locations = [
#     "Nội Bài",
#     "Qua 50m đối diện ngã 3 vào thôn Điền Xá",
#     "Qua Ngã Tư Cao Tốc TL - Phúc Yên - Km 11+380 Cao Tốc BTL-NB",
#     "Soát vé cao tốc Bắc Thăng Long",
#     "Đối Diện Nhà Máy Tấm Lợp Vitmetal- Km 8+700 Cao Tốc BTL-NB",
#     "KCN Quang Minh",
#     "Đối diện Công ty cơ khí Nam Hồng",
#     "Qua cầu vượt ngã 4 Nam Hồng 70m Cao tốc BTL",
#     "Đầm Vân Trì",
#     "Qua cầu chui dân sinh số 4 - đối diện đường vào thôn Nhuế, Km 11+200",
#     "UBND xã Kim Chung",
#     "Trước ngã tư khu CN Thăng Long 100m",
#     "KCN Bắc Thăng Long",
#     "96 Phạm Văn Đồng",
#     "Showroom Ô Tô Trung Sơn (Đối Diện 315 Phạm Văn Đồng)",
#     "Trước 100m ngõ 218 Phạm Văn Đồng",
#     "370 Phạm Văn Đồng",
#     "Siêu thị Metro Thăng Long",
#     "Đối diện 36A Phạm Văn Đồng",
#     "Bộ Công An, 47 Phạm Văn Đồng, Mai Dịch, Bắc Từ Liêm, Hà Nội, Việt Nam",
#     "Trạm trung chuyển xe buýt Hoàng Quốc Việt (cột sau)",
#     "Học viện Chính trị Quốc Gia Hồ Chí Minh",
#     "Cao Đẳng Sư Phạm Mẫu Giáo Trung Ương - 387 Hoàng Quốc Việt",
#     "247-249 Hoàng Quốc Việt",
#     "Công viên Nghĩa Đô",
#     "165 Cầu Giấy",
#     "Điểm trung chuyển Cầu Giấy - GTVT 01",
#     "Cầu Giấy - Tuyến 07"
# ]


# locations = [
#     "CV Thống Nhất",
#     "Công viên Thống Nhất",
#     "55 Quang Trung",
#     "67 Trần Hưng Đạo",
#     "Nhà hát Lớn Hà Nội",
#     "Ngân hàng Nhà nước Việt Nam - Vườn hoa con Cóc",
#     "23 Hàng Tre - Ngã 4 Lò Sũ",
#     "Hàng Muối - Cầu Chương Dương",
#     "Ô Quan Chưởng",
#     "Chùa Ái Mộ",
#     "52 Ngọc Lâm",
#     "170 Ngọc Lâm",
#     "Đối diện 447 Ngọc Lâm",
#     "Phòng Công Chứng số 2 TPHN",
#     "Cây xăng số 84 Cầu Chui (BĐX Gia Thụy)",
#     "Đối diện Savico MegaMall Long Biên",
#     "Đối Diện Công Ty Nước Sạch - Nguyễn Văn Linh",
#     "Đối diện UBND phường Phúc Đồng",
#     "523 Nguyễn Văn Linh - Khu CN Sài Đồng",
#     "693 Nguyễn Văn Linh - ngã 3 Thạch Bàn",
#     "Đối Diện Công Ty May 10 - Nguyễn Văn Linh",
#     "Ngã 3 cầu Thanh Trì - Nguyễn Đức Thuận",
#     "Bưu cục Trâu Quỳ",
#     "Ngã 3 Ngô Xuân Quảng - Nguyễn Mậu Tài",
#     "Cửa hàng Xăng dầu số 100 - 234 Ngô Xuân Quảng",
#     "Số 14 đường Học Viện Nông Nghiệp",
#     "Học viện Nông Nghiệp Việt Nam"
# ]

# locations = [
#     "Học viện Nông Nghiệp Việt Nam",
#     "Công Ty Tư Vấn Dịch Vụ Khoa Học Nông Nghiệp - Ngô Xuân Quảng",
#     "Cửa hàng Xăng dầu số 100 - 255 Ngô Xuân Quảng",
#     "Nhà văn hóa TDP Chính Trung - 139 Ngô Xuân Quảng",
#     "Bưu cục Trâu Quỳ",
#     "Gần Ngã Ba Cầu Thanh Trì - Nguyễn Đức Thuận",
#     "Qua Ngã 3 Cầu Thanh Trì - Nguyễn Văn Linh",
#     "Công Ty May 10 - Nguyễn Văn Linh",
#     "Số 707 Nguyễn Văn Linh",
#     "Công Ty Thí Nghiệm Miền Bắc - 465 Nguyễn Văn Linh",
#     "UBND phường Phúc Đồng",
#     "105 - 107 Nguyễn Văn Linh",
#     "Hè Trước Savico Megamall - Nguyễn Văn Linh",
#     "MediaMart Long Biên",
#     "589 Nguyễn Văn Cừ",
#     "549 Nguyễn Văn Cừ",
#     "Bến xe Gia Lâm",
#     "171 - 173 Ngọc Lâm",
#     "Đối diện chùa Ái Mộ",
#     "Ô Quan Chưởng",
#     "Ngã 4 Nguyễn Hữu Huân - Hàng Mắm",
#     "Cung thiếu Nhi Hà Nội",
#     "40 Ngô Quyền",
#     "Thư viện Hà Nội",
#     "KS Melia",
#     "54 Lý Thường Kiệt",
#     "Ga Hà Nội",
#     "CV Thống Nhất"
# ]

# locations = [
#     "Đại học Thủ đô Hà Nội",
#     "Cầu Dịch Vọng",
#     "Ngõ 9 - Đào Tấn (Công viên Thủ Lệ)",
#     "Hồ Ngọc Khánh",
#     "Đối diện Đại học Luật Hà Nội",
#     "57A Huỳnh Thúc Kháng",
#     "7 Huỳnh Thúc Kháng",
#     "171 Thái Hà",
#     "161-163 Thái Hà",
#     "3 Thái Hà-Bể bơi Thái Hà",
#     "251 Chùa Bộc",
#     "21 Chùa Bộc",
#     "20 Tôn Thất Tùng",
#     "Trước Tòa Nhà Artemis - Đường Tôn Thất Tùng Kéo Dài",
#     "150 Lê Trọng Tấn",
#     "Nhà Công Vụ QC PKKQ - 210 Lê Trọng Tấn",
#     "Đối diện siêu thị ACE Mart",
#     "Công viên Định Công",
#     "Đối diện Chợ xanh Định Công",
#     "Đối diện 807 Giải Phóng",
#     "Bến xe Giáp Bát",
#     "Ga Giáp Bát",
#     "Ngã 3 Giải Phóng - Linh Đàm",
#     "Đối Diện Tập Thể Bến Xe Nước Ngầm Hà Nội - Ngọc Hồi",
#     "Trường PTTH Việt Nam Balan (Đối diện Khách sạn Nam Thành)",
#     "Qua đường vào Bệnh viện đa khoa Thăng Long 60m",
#     "Đối diện TCT cơ điện nông nghiệp & Thủy lợi (Văn Điển)",
#     "Đối diện Trụ sở HĐND huyện Thanh Trì",
#     "Qua ngã 3 Ngọc Hồi",
#     "Qua Khu Tập Thể LICÔLA 100M - Ngọc Hồi",
#     "Gần ngã 3 đường Quỳnh Đô",
#     "Qua Công Ty CP Vận Tải & Dịch Vụ TS 15M - Ngọc Hồi",
#     "Viện nghiên cứu trồng & phát triển cây thuốc",
#     "Chùa Ngọc Hồi",
#     "Đối diện trường THCS Ngọc Hồi",
#     "Trước ngã 3 Lạc Thị 200m",
#     "Qua Chợ Lạc Thị 200m",
#     "Qua lối vào Chùa Thanh Dương 100m",
#     "Đại lý thuốc tân dược thôn Vĩnh Thịnh",
#     "Cổng làng Vĩnh Trung",
#     "(B) Khánh Hà"
# ]

locations = [
    "(B) Khánh Hà",
    "Đối diện cổng làng Vĩnh Trung",
    "Đối diện đại lý thuốc tân dược thôn Vĩnh Thịnh",
    "Đối diện lối vào Chùa Thanh Dương 100m",
    "Cách Chợ Lạc Thị 100m",
    "Qua ngã 3 Lạc Thị 150m",
    "Trường THCS Ngọc Hồi",
    "Đối diện Chùa Ngọc Hồi",
    "Công ty công trình giao thông 124 (Km 12 + 500 Quốc lộ 1A)",
    "Công ty 17 Lữ đoàn 17 Binh đoàn 12 - Ngọc Hồi",
    "Qua ngã 3 đường Quỳnh Đô",
    "Đối diện Khu tập thể LICÔLA",
    "449 - 451 Ngọc Hồi",
    "373 Ngọc Hồi",
    "TCT cơ điện nông nghiệp & Thủy lợi (Văn Điển)",
    "Đối diện 184 Ngọc Hồi",
    "Công Ty Biến Thế ABB - Ngọc Hồi",
    "Bến xe Nước Ngầm",
    "Ngã 3 Giải Phóng - Linh Đàm",
    "Dải đỗ số 3 bến xe Giáp Bát",
    "Toyota Giải Phóng",
    "352 Giải Phóng",
    "Trạm biến áp số 9 Định Công",
    "Đối diện trạm cấp nước sạch Định Công",
    "Kiốt số 7 nhà CT.6 - ĐN 2 Định Công",
    "Đối diện 210 Lê Trọng Tấn",
    "Đối diện 158 Lê Trọng Tấn",
    "Cạnh Hàng Rào Bảo Tàng Không Quân - Đường Tôn Thất Tùng Kéo Dài",
    "Đại Học Y Hà Nội",
    "Học Viện Ngân Hàng",
    "54 Thái Hà",
    "176 Thái Hà",
    "Rạp chiếu phim Quốc Gia",
    "Đối diện Đài Truyền hình Hà Nội",
    "20 Huỳnh Thúc Kháng",
    "89 Nguyễn Chí Thanh",
    "Học viện Hành chính Quốc gia",
    "10 Đào Tấn - Viện Vật lý",
    "Cầu Dịch Vọng",
    "Đại học Thủ đô Hà Nội",
    "(A) CV Nghĩa Đô"
]




def get_coordinates(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

def insert_into_db(name, lat, lng):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    add_station = ("INSERT INTO bus_routing_busstation "
                   "(name, latitude, longitude, bus_number, direction, created_at, updated_at) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data_station = (name, lat, lng, "12", 1, datetime.now(), datetime.now())
    cursor.execute(add_station, data_station)
    conn.commit()
    cursor.close()
    conn.close()

for location in locations:
    lat, lng = get_coordinates(location)
    if lat and lng:
        insert_into_db(location, lat, lng)
        # print(f"Inserted {location} with coordinates ({lat}, {lng})")
    else:
        print(f"Failed to get coordinates for {location}")
