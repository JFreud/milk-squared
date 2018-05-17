<VirtualHost *:80>
             ServerName 204.48.24.108

             WSGIScriptAlias / /var/www/deploytest/deploytest.wsgi

             <Directory /var/www/deploytest/deploytest/>
                        Order allow,deny
                        Allow from all
             </Directory>

             Alias /static /var/www/deploytest/deploytest/static
             <Directory /var/www/deploytest/deploytest/static/>
                        Order allow,deny
                        Allow from all
            </Directory>

</VirtualHost>
