server {
% if 'listens' in config:
  % for listen in config['listens']:
  listen ${listen};
  % endfor
% else:
  include "listens.conf";

  % if 'ssl' in config:
  include "listens-ssl.conf";
  % endif
% endif

  % if 'ssl' in config:
  ssl_certificate ssl/${config['host']}.crt;
  ssl_certificate_key ssl/${config['host']}.key;
  % endif

  server_name "${config['host']}";

  location / {
  	proxy_pass "http://localhost:${port}";
  }
}