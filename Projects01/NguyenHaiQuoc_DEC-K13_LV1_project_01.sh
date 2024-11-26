#!/bin/bash

input_file="$1"

if [[ -z "$input_file" || ! -f "$input_file" ]]; then
  echo "File không tồn tại. Vui lòng kiểm tra lại đường dẫn."
  exit 1
fi

required_fields=(
  "id" "imdb_id" "popularity" "budget" "revenue" "original_title"
  "cast" "homepage" "director" "tagline" "keywords" "overview"
  "runtime" "genres" "production_companies" "release_date"
  "vote_count" "vote_average" "release_year" "budget_adj" "revenue_adj"
)

header=$(awk -F',' 'NR==1 {print}' "$input_file")
IFS=',' read -r -a header_fields <<< "$header"

for field in "${required_fields[@]}"; do
  if [[ ! " ${header_fields[*]} " =~ $field ]]; then
    echo "Thiếu trường dữ liệu: $field"
    exit 1
  fi
done

# 1. Sắp xếp phim theo ngày phát hanh
awk 'BEGIN {FS=OFS="\""} {for (i=2; i<=NF; i+=2) gsub(/,/, "#", $i)} 1' "$input_file" | \
awk -F',' 'NR > 1 {split($16, d, "/");
year = d[3] + 0;
if (year >= 25 && year <= 99) year = 1900 + year; 
else if (year >= 0 && year <= 24) year = 2000 + year; 
print year"-"d[1]"-"d[2] "," $6}' | sort -t',' -k1,1 > sortedMoviesByReleaseDay.txt

# 2. Lọc phim có đánh giá cao hơn 7.5
awk 'BEGIN {FS=OFS="\""} {for (i=2; i<=NF; i+=2) gsub(/,/, "#", $i)} 1' "$input_file" | \
awk -F',' 'NR > 1 && $18 > 7.5 {print $6 "," $18}' > greaterThan7.5VoteAverageMovie.txt

# 3. Phim có doanh thu cao nhất và thấp nhất
max=$(awk -F',' 'NR > 1 && $5 ~ /^[0-9]+(\.[0-9]+)?$/ {if ($5 > max || max == "") max=$5} END {print max}' "$input_file")
echo -e "Phim có doanh thu cao nhất:\n"
awk -F',' -v max="$max" 'NR > 1 && $5 == max {print $6 "," $5}' "$input_file"

min=$(awk -F',' 'NR > 1 && $5 ~ /^[0-9]+(\.[0-9]+)?$/ {if (min == "" || $5 < min) min=$5} END {print min}' "$input_file")
echo -e "Phim có doanh thu thấp nhất:\n"
awk -F',' -v min="$min" 'NR > 1 && $5 == min {print $6 "," $5}' "$input_file"

# 4. Tổng doanh thu
echo -e "\nTổng doanh thu:\n"
awk -F',' 'NR > 1 && $5 ~ /^[0-9]+$/ {total += $5} END {print total}' "$input_file"

# 5. Top 10 phim lợi nhuận cao nhat
echo -e "\nTop 10 phim lợi nhuận cao nhất:\n"
awk -F',' 'NR > 1 && $4 ~ /^[0-9]+$/ && $5 ~ /^[0-9]+$/ {print $6 "," $5-$4}' "$input_file" | sort -t',' -k2,2nr | head -n 10 

# 6. Đạo diễn và diễn viên có nhiều phim nhất
echo -e "\nĐạo diễn có nhiều bộ phim nhất:\n"
awk -F',' 'NR > 1 {print $9}' "$input_file" | sed 's/|/\n/g' | awk 'length($0) > 0' | sort | uniq -c | sort -nr | head -n 1 

echo -e "\nDiễn viên đóng nhiều phim nhất:\n"
awk -F',' 'NR > 1 {print $7}' "$input_file" | sed 's/|/\n/g' | awk 'length($0) > 0' | sort | uniq -c | sort -nr | head -n 1

# 7. Thống kê số lượng phim theo thể loại
echo -e "\nThống kê số lượng phim theo thể loại:\n"
awk 'BEGIN {FS=OFS="\""} {for (i=2; i<=NF; i+=2) gsub(/,/, "#", $i)} 1' "$input_file" | awk -F',' 'NR > 1 {print $14}' | sed 's/|/\n/g' | sort | uniq -c | sort -nr | awk 'length($2) > 0 {print $2, $1}'


#Từ những trường dữ liệu của tập dữ liệu tmdb-movies.csv, ta có thể mở rộng thêm một số phân tích sau:
#1.Thông qua genres và release_date, có thể suy ra được xu hướng ra các thể loại phim theo thời gian, theo mùa
#2.Thông qua budget, revenue, genres có thể phân tích được sự đầu tư và lợi nhuận từ thể loại phim nào có trung bình lớn hơn
#3.Thông qua popularity, genres phân tích được thể loại phim nào có độ phổ biến trung bình cao nhất, thể loại nào ít được quan tâm nhất
#4.Thông qua cast, budget tìm ra được diễn viên nào được tham gia vào các dự án có chi phi đầu tư từ một mốc cụ thể nào đấy trở lên nhiều nhất, ít nhất
#5.Từ runtime và genres để tìm ra thể loại film nào có trung bình thời lượng dài nhất, ngắn nhất hoặc so sánh với một mốc cụ thể
#…
