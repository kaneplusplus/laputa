cnidaria
===

A parallel computing framework for the elr package based on Redis.

Description
---

cnidaria is a python package that provides an elastic, fault-tolerant,
parallel computing foundation for the elr (ensemble learners with Redis) 
package. 

Requirements
---

To use the cnidaria package you will need Python (tested on version 2.7), 
the redis python package, and a connection to an instance of Redis.
For further information about Redis, see the [homepage](http://redis.io).

Installing cnidaria
---

The easiest way to install cnidaria uses pip in a shell:

```bash
> pip install -e git+https://github.com/kaneplusplus/cnidaria.git#egg=cnidaria
```

This package can also be installed with pip in a shell using the following 
commands:

```bash
> find . -name "*.pyc" -print | xargs rm
> pip uninstall cnidaria
> python setup.py sdist
> pip install dist/cnidaria-0.1.tar.gz
``` 

Using cnidaria
---

The cnidaria package should currently be considered "plumbing" for the
elr package. When the interface stabilizes and the features are expanded 
a more complete user's guide will be added.

Support
---

1. cnidaria is supported on Python version 2.7.
2. The development home of this project can be found at: [https://github.com/kaneplusplus/cnidaria](https://github.com/kaneplusplus/cnidaria)
3. Contributions are welcome.
4. For more information contact Michael Kane at [kaneplusplus@gmail.com](kaneplusplus@gmail.com).
