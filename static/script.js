// =========================
// ScamShield AI
// =========================

// Animate Risk Percentage
window.addEventListener("load", () => {

    const score = document.querySelector(".circle span");

    if (score) {

        let target = parseInt(score.innerText);

        let count = 0;

        score.innerText = "0%";

        let interval = setInterval(() => {

            count++;

            score.innerText = count + "%";

            if (count >= target) {

                clearInterval(interval);

            }

        }, 20);

    }

});


// =========================
// Auto Scroll to Result
// =========================

window.addEventListener("load", () => {

    const result = document.querySelector(".result-card");

    if (result) {

        result.scrollIntoView({

            behavior: "smooth"

        });

    }

});


// =========================
// Loading Button Animation
// =========================

const form = document.querySelector("form");

if (form) {

    form.addEventListener("submit", () => {

        const btn = form.querySelector("button");

        btn.disabled = true;

        btn.innerHTML = "⏳ Analyzing...";

    });

}


// =========================
// Textarea Character Counter
// =========================

const areas = document.querySelectorAll("textarea");

areas.forEach(area => {

    area.addEventListener("input", () => {

        if (area.value.length > 2000) {

            alert("Maximum 2000 characters allowed.");

            area.value = area.value.substring(0, 2000);

        }

    });

});


// =========================
// Drag & Drop Highlight
// =========================

const fileInput = document.querySelector("input[type=file]");

if(fileInput){

fileInput.addEventListener("dragover",()=>{

fileInput.style.border="2px dashed #4F8EF7";

});

fileInput.addEventListener("dragleave",()=>{

fileInput.style.border="none";

});

}