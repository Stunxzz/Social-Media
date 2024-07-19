document.addEventListener("DOMContentLoaded", function () {
            const toggleButton = document.getElementById('user-icon');
            const closeButton = document.getElementById('close-sidebar');
            const sidebar = document.getElementById('side-bar');
            // const mainContent = document.getElementById('main-content');

            toggleButton.addEventListener('click', function () {
                sidebar.style.display = 'block';
                // mainContent.classList.add('shifted');
            });

            closeButton.addEventListener('click', function () {
                sidebar.style.display = 'none';
                // mainContent.classList.remove('shifted');
            });
        });

        function toggleComments(button) {
            const commentsDiv = button.parentElement.nextElementSibling;
            commentsDiv.style.display = commentsDiv.style.display === 'none' ? 'block' : 'none';
        }