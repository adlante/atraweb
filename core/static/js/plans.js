// اسکریپت مخصوص صفحه پلن‌ها (جهت ذخیره در حافظه و انتقال کاربر)
function addPlanToProforma(event, redirectUrl, planSlug, planTitle, planPrice) {
    // ۱. متوقف کردن انتقال فوری مرورگر (جلوگیری از Race Condition)
    event.preventDefault();

    // ۲. ساختاردهی اطلاعات پلن جدید
    const newPlan = {
        id: planSlug,
        title: planTitle,
        price: planPrice,
        suffix: 'تومان' // می‌توانید پسوند را هم به صورت پویا پاس بدهید
    };

    // ۳. خواندن آرایه پلن‌های قبلی از حافظه
    let proformaPlans = JSON.parse(localStorage.getItem('proforma_plans')) || [];

    // ۴. بررسی تکراری نبودن پلن (اگر کاربر دو بار روی یک پلن کلیک کرد، دو بار اضافه نشود)
    const exists = proformaPlans.some(plan => plan.id === newPlan.id);
    if (!exists) {
        proformaPlans.push(newPlan);
        localStorage.setItem('proforma_plans', JSON.stringify(proformaPlans));
    }

    // ۵. حالا که خیالمون از ذخیره داده‌ها راحته، کاربر رو به آدرس مقصد هدایت می‌کنیم
    window.location.href = redirectUrl;
}
