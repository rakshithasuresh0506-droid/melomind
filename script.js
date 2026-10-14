/* =====================================================
   MELOMIND JAVASCRIPT
===================================================== */

document.addEventListener("DOMContentLoaded", function () {


    /* =================================================
       SMOOTH SCROLL
    ================================================= */

    const links = document.querySelectorAll(
        'a[href^="#"]'
    );


    links.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId =
                this.getAttribute("href");


            if (targetId === "#") {
                return;
            }


            const target =
                document.querySelector(targetId);


            if (target) {

                event.preventDefault();


                target.scrollIntoView({

                    behavior: "smooth",

                    block: "start"

                });

            }

        });

    });



    /* =================================================
       MODULE CARD ANIMATION
    ================================================= */

    const cards =
        document.querySelectorAll(".module-card");


    const cardObserver =
        new IntersectionObserver(

            function (entries) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.style.opacity = "1";

                        entry.target.style.transform =
                            "translateY(0)";

                    }

                });

            },

            {
                threshold: 0.12
            }

        );


    cards.forEach(function (card, index) {

        card.style.opacity = "0";

        card.style.transform =
            "translateY(25px)";


        card.style.transition =
            "opacity .6s ease " +
            (index * 0.08) +
            "s, transform .6s ease " +
            (index * 0.08) +
            "s, box-shadow .35s ease";


        cardObserver.observe(card);

    });



    /* =================================================
       NAVBAR ACTIVE SECTION
    ================================================= */

    const sections =
        document.querySelectorAll("section[id]");


    const navLinks =
        document.querySelectorAll("nav a");


    window.addEventListener("scroll", function () {


        let currentSection = "";


        sections.forEach(function (section) {

            const sectionTop =
                section.offsetTop - 200;


            const sectionBottom =
                sectionTop + section.offsetHeight;


            if (
                window.scrollY >= sectionTop &&
                window.scrollY < sectionBottom
            ) {

                currentSection =
                    section.getAttribute("id");

            }

        });


        navLinks.forEach(function (link) {

            link.classList.remove("active");


            if (
                link.getAttribute("href") ===
                "#" + currentSection
            ) {

                link.classList.add("active");

            }

        });

    });


});