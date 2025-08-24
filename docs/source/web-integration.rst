Web Integration
===============

Webpage
-------

Embed the widget in any HTML page:

.. code-block:: html

   <script src="https://circassiandna-chatbot.onrender.com/static/chat-widget.js"></script>
   <div id="chatbot"></div>
   <script>
     window.onload = function() {
       ChatWidget.init({
         apiUrl: 'https://circassiandna-chatbot.onrender.com/api/chat',
         containerId: 'chatbot',
       });
     };
   </script>

Refer :doc:`web` for chat widget code and CSS style.


WordPress / PHP
---------------

Use ``chatbot-widget-global-web.php`` to register a ``wp_footer`` hook that injects
the widget site-wide. Drop it into your theme or a small custom plugin (see :doc:`web`).