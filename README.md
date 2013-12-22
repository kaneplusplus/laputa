laputa
===

A parallel computing framework for the stat\_agg package based on Redis.

Description
---

laputa is a python package that provides an elastic, fault-tolerant,
parallel computing foundation for the stat\_agg (statistical aggregates)
package. 

Requirements
---

To use the laputa package you will need Python (tested on version 2.7), 
the redis python package, and a connection to an instance of Redis.
For further information about Redis, see the [homepage](http://redis.io).

Installing laputa
---

The easiest way to install laputa uses pip in a shell:

```bash
> pip install -e git+https://github.com/kaneplusplus/laputa.git#egg=laputa
```

This package can also be installed with pip in a shell using the following 
commands:

```bash
> find . -name "*.pyc" -print | xargs rm
> pip uninstall laputa
> python setup.py sdist
> pip install dist/laputa-0.1.tar.gz
``` 

Using laputa
---

The laputa package should currently be considered "plumbing" for the
elr package. When the interface stabilizes and the features are expanded 
a more complete user's guide will be added.

Support
---

1. laputa is supported on Python version 2.7.
2. The development home of this project can be found at: [https://github.com/kaneplusplus/laputa](https://github.com/kaneplusplus/laputa)
3. Contributions are welcome.
4. For more information contact Michael Kane at [kaneplusplus@gmail.com](kaneplusplus@gmail.com).
