ایزی‌بلاگ: تامام تامام
---

این یک سازندهٔ سایت استاتیک است که خیلی ساده و آسون و سریعه.

# نصب

اول وابستگی‌ها باید نصب بشوند. این‌ها هستند:

```bash
pip install jdatetime markdown-it-py
```

بعد این مخزن رو در جایی بارگیری کنید. مثلاً با گیت:

```bash
git clone https://github.com/ekm507/easyblog
cd easyblog
```

# استفاده

حالا وقتشه به مسیر پوشه نگاه کنیم:
```bash
tree
```
خروجی:
```
├── content
│   ├── img
│   │   └── new.jpg
│   ├── new.md
├── generate.py
├── output
├── README.md
└── theme
    ├── index.html
    ├── index_post_list.html
    ├── index_stylesheet.css
    ├── post.html
    └── post_stylesheet.css
```

خب. اولاً که در مسیر اصلی ما ابزار `generate.py` رو داریم ما چند تا مسیر داریم. هر موقع اون رو اجرا کنی در مسیر `output` سایت ساخته می‌شه. یعنی فایل `index.html` و بقیهٔ فایل‌ها همه داخل همون پوشه هستند.

از بین مسیرها مهم‌ترینشون مسیر `content` است که مطالب وبلاگ رو با فرمت مارک‌داون توش می‌نویسی. فقط یه سربرگ هم باید داشته باشه که مثل اینه:

```md
عنوان: فلان
تاریخ: ۱۴۰۲-۱۱-۱۲
---
```

یعنی می‌نویسی `عنوان:` و بعد عنوان. بعد می‌نویسی `تاریخ:` و بعد تاریخ در همین فرمت. تهش هم سه تا خط تیره می‌ذاری `---` و تمام. زیرش فایل اصلی مارک‌داون رو می‌نویسی.

هر چی عکس خواستی بذار توی همون مسیر `content/img` و بهشون لینک بده. این مسیر با همهٔ محتواهایش داخل مسیر `output` کپی خواهد شد.

مسیر دیگر `theme` است که توش ۵ تا فایل داره که زمینهٔ سایت رو مشخص می‌کنند.

فایل `index.html` رو ویرایش کن و مثلاً بخش `title` رو توش عوض کن. یه جایی داره که با حرف بزرگ انگلیسی نوشته `POSTS`. عنوان مطالبت در اونجا قرار خواهند گرفت. خودکار.

بعد فایل `index_post_list.html` رو هم داریم که قالبی برای عنوان هر پسته. توش یه بخش تاریخ و یه بخش عنوان داره.

و فایل `post.html` هم قالبیه که خود پست داخلش قرار می‌گیره. در این هم باید بخش‌هایی مثل `title` رو ویرایش کنی. بخش `POST` هم جاییه که متن پست داخلش قرار خواهد گرفت.

۲ تا فایل `CSS` هم داریم که برای استایل‌های سایت هستند.

همین!

## استفادهٔ سریع

مطالب رو در فایل‌های مارک‌داون در مسیر `content` قرار بده و بهشون یه سربرگ هم اضافه کن. فایل `generate.py` رو اجرا کن و خروجی سایت رو در مسیر `output` ببین.

تامام
