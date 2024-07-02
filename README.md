<div dir="rtl">

# kenar-api
## درباره
این کتابخانه برای استفاده ی راحت‌تر و سریع‌تر از سرویس های کنار دیوار توسعه داده شده است.
>توجه: برای استفاده از این کتابخانه باید نیازمند نسخه ی پایتون بالاتر از 3.10 هستید. 

## ویژگی های اصلی
* تولید آدرس ریدایرکت به احراز باز برای دریافت دسترسی ها از کاربر
* امکان ارسال پیام در چت دیوار و ثبت درخواست برای مطلع شدن از پیام های چت دیوار روی یک آگهی
* امکان درج/حذف/دریافت افزونه در آگهی های دیوار
* امکان درج/حذف/دریافت افزونه روی دسته ای از آگهی های یک کاربر (بر اساس دسته بندی آگهی)

## نحوه ی نصب 
برای این منظور میتوانید از پکیج منیجر [pip](https://pypi.org/project/Kenar) استفاده کنید

<div dir="ltr">

```bash
pip install Kenar
```
</div>

## راهنمای استفاده
پس از ساخت برنامه در پنل کنار و گرفتن کلید API و کلید محرمانه OAuth مربوط به آن ، با قرار دادن این فیلد ها در environment variable های پروژه ی خود ، میتوانید از این SDK استفاده کنید.  
- [نمونه ساخت اپ](https://github.com/divar-ir/kenar-api/blob/main/samples/sample_app.py)
- [نمونه ساخت ریدایرکت احراز باز و گرفتن اکسس توکن احراز](https://github.com/divar-ir/kenar-api/blob/main/samples/sample_oauth.py)
- [نمونه ساخت افزونه آگهی و کاربر](https://github.com/divar-ir/kenar-api/blob/main/samples/sample_addon.py)
- [نمونه سرچ آگهی با فیلتر، دریافت اطلاعات یک آگهی، آگهی های کاربر و اطلاعات شماره تلفن کاربر](https://github.com/divar-ir/kenar-api/blob/main/samples/sample_finder.py)
- [نمونه ارسال پیام در چت و اجازه دریافت پیام ها روی یک آگهی](https://github.com/divar-ir/kenar-api/blob/main/samples/sample_chat.py)

به عنوان نمونه ، برای ساخت کلاینت کنار، نیاز است متغیر های محیطی `KENAR_APP_SLUG` (با مقدار برابر با شناسه یکتای برنامه) و `KENAR_API_KEY`(برابر با کلید محرمانه دریافت شده برای برنامه) ، `KENAR_OAUTH_SECRET` (برابر با کلید محرمانه ی OAuth) و `KENAR_OAUTH_REDIRECT_URL` (برابر با لینک بازگشت احراز باز) ست شوند و از طریق نمونه کد زیر کلاینت ساخته شود.


<div dir="ltr">

```python
import os
from kenar import ClientConfig, Client

client_conf = ClientConfig(
    app_slug=os.environ.get("KENAR_APP_SLUG"),
    api_key=os.environ.get("KENAR_API_KEY"),
    oauth_secret=os.environ.get("KENAR_OAUTH_SECRET"),
    oauth_redirect_url=os.environ.get("KENAR_OAUTH_REDIRECT_URL"),
)

kenar_client = Client(client_conf)
```
</div>

پس از ساخت کلاینت میتوان از تمام سرویس های نام برده ، با فراخوانی property مربوطه ، استفاده کرد. به عنوان مثال برای آپلود عکس میتوان از کد زیر بهره گرفت:

<div dir="ltr">

```python
rsp = kenar_client.addon.upload_image("PATH_TO_FILE")
```

</div>

## پیشنهادات برای بهبود
پذیرای هر گونه پیشنهادات شما برای بهتر کردن این کتاب‌خانه هستیم. در قسمت [issues](https://github.com/divar-ir/kenar-api/issues) پروژه میتوانید مسائل خود را با ما مطرح کنید.

## ادرس پنل توسعه دهندگان
[کنار دیوار](https://divar.ir/kenar)

## مستندات کنار دیوار
در صورتی که از زبان پایتون برای توسعه ی برنامه خود استفاده نمیکنید ، میتوانید با بهره گیری از [مستندات کنار دیوار](https://github.com/divar-ir/kenar-docs) مستقیما اندپوینت های سرویس را فراخوانی کند.
</div>