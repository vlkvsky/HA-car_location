[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# livegpstracks car tracker integration

<h1>Description</h1>
<p>This integration allows you to connect any GPS Tracker ( compatible with <a href='https://livegpstracks.com/'>livegpstracks</a> service) to HomeAssistant.</p>

<h1>Installation</h1>
<p>You need to register in the livegpstracks service and connect the tracker (the site has detailed instructions for various models) to it. After that, through the toolbar on the site we create a private link for tracking. The link looks like:</p> 
<pre><code>
https://livegpstracks.com/dv_USERID.html
</code></pre>
<p>here USERID – is ID of your livegpstracks share, it will be needed to us further </p>
<p>Place the "car_location" folder to "config_folder_homeassistant/custom_components/". Do not forget about the rights to created folders and files.</p>

<h1>Configuration</h1>
<p>Add the following lines in the "configuration.yaml" file:</p>
<pre><code>
car_location:
  username: 'your_username'
  client_id: 'your_share_id'
</code></pre>
<p>here "your_username" is the username, you registered with on livegpstracks, "your_share_id" is ID of your livegpstracks share.</p>