# Yaks Python examples

## Prerequisites

   The [Zenoh](https://zenoh.io) C client library and Python API must be installed on your host.
   See installation instructions on https://zenoh.io or clone, build and install it yourself from https://github.com/atolab/zenoh-c and https://github.com/atolab/zenoh-python.

## Start instructions
   
   ```bash
   python3 <example.py>
   ```

## Examples description

### yaddstorage

   Add a storage in the Yaks service it's connected to.

   Usage:
   ```bash
   python3 yaddstorage.py [selector] [storage-id] [locator]
   ```
   where the optional arguments are:
   - **selector** :  the selector matching the keys (path) that have to be stored.  
                     Default value: `/demo/example/**`
   - **storage-id** : the storage identifier.  
                      Default value: `Demo` 
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.

   Note that his example doesn't specify the Backend that Yaks has to use for storage creation.  
   Therefore, Yaks will automatically select the memory backend, meaning the storage will be in memory
   (i.e. not persistent).

### yput

   Put a key/value into Yaks.  
   The key/value will be stored by all the storages with a selector that matches the key.
   It will also be received by all the matching subscribers (see [ysub](#ysub) below).  
   Note that if no storage and no subscriber are matching the key, the key/value will be dropped.
   Therefore, you probably should run [yaddstorage](#yaddstorage) and/or [ysub](#ysub) before YPut.

   Usage:
   ```bash
   python3 yput.py [path] [value] [locator]
   ```
   where the optional arguments are:
   - **path** : the path used as a key for the value.  
                Default value: `/demo/example/yaks-python-put` 
   - **value** : the value (as a string).  
                Default value: `"Put from Yaks Python!"` 
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.

### yget

   Get a list of keys/values from Yaks.  
   The values will be retrieved from the Storages containing paths that match the specified selector.  
   The Eval functions (see [yeval](#yeval) below) registered with a path matching the selector
   will also be triggered.

   Usage:
   ```bash
   python3 yget.py [selector] [locator]
   ```
   where the optional arguments are:
   - **selector** : the selector that all replies shall match.  
                    Default value: `/demo/example/**` 
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.

### yremove

   Remove a key and its associated value from Yaks.  
   Any storage that store the key/value will drop it.  
   The subscribers with a selector matching the key will also receive a notification of this removal.

   Usage:
   ```bash
   python3 yremove [path] [locator]
   ```
   where the optional arguments are:
   - **path** : the key to be removed.  
                Default value: `/demo/example/yaks-python-put` 
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.

### ysub

   Register a subscriber with a selector.  
   The subscriber will be notified of each put/remove made on any path matching the selector,
   and will print this notification.

   Usage:
   ```bash
   python3 ysub.py [selector] [locator]
   ```
   where the optional arguments are:
   - **selector** : the subscription selector.  
                    Default value: `/demo/example/**` 
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.

### yeval

   Register an evaluation function with a path.  
   This evaluation function will be triggered by each call to a get operation on Yaks 
   with a selector that matches the path. In this example, the function returns a string value.
   See the code for more details.

   Usage:
   ```bash
   python3 yeval.py [selector] [locator]
   ```
   where the optional arguments are:
   - **path** : the eval path.  
                Default value: `/demo/example/yaks-python-eval` 
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.

### ythr_pub & ythr_sub

   Pub/Sub throughput test.
   This example allows to perform throughput measurements between a pubisher performing
   put operations and a subscriber receiving notifications of those put.
   Note that you can run this example with or without any storage.

   Publisher usage:
   ```bash
   python3 ythr_pub.py <payload-size> [locator]
   ```
   where the arguments are:
   - **payload-size** : the size of the payload in bytes.  
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.

   Subscriber usage:
   ```bash
   python3 ythr_sub.py [locator]
   ```
   where the optional arguments are:
   - **locator** : the locator of the Yaks service to connect.  
                   Default value: none, meaning the Yaks service is found via multicast.
