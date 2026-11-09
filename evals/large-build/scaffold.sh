mkdir -p dist/photos
printf '%s\n' '<!doctype html><title>Wedding photos</title><h1>Our wedding</h1>' > dist/index.html
i=1
while [ "$i" -le 300 ]; do
  head -c 40000 /dev/urandom > "dist/photos/photo-$i.jpg"
  i=$((i + 1))
done
