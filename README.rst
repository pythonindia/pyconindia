Publicity Mail Usage
====================

The command line syntax of the tool is as given below.
The `-c`, `-s` and `-t` options are mandatory::

  usage: publicitymail [-h] [-c CONFIG] [-s SUBJECT] [-t TEMPLATE]

  optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG, --config CONFIG
                          Configguration file
    -s SUBJECT, --subject SUBJECT
                          Mail subject
    -t TEMPLATE, --template TEMPLATE
                          Mail body template

An example configuration file is available at `conf/example1.cfg`.
An example template file is available at `conf/example1.template`.

Any value inside the configuration can be overriden using a specially
formatted environment variable. The environment variable name should
be in this format: PUBLICITY_<SECTION>_<KEY>

For example, to override the value of `password` inside the `main` section,
set an environment variable named `PUBLICITY_MAIN_PASSWORD` like this::

  export PUBLICITY_MAIN_PASSWORD=the-real-password

Once the configuration file and template is ready, a mail can be send like
this::

  publicitymail -c /path/to/config.cfg -s "The mail subject" -t /path/to/some.template

It is reccommened to use separate configuration and template for different mails.

The configuration
-----------------

This is example configuration::

  [main]
  username = baiju.m.mail@gmail.com
  password = this-is-wrong-password
  from_email = baiju.m.mail@gmail.com
  from_name = Baiju Muthukadan

  [to_addresses]
  bangpypers@python.org = Bangalore
  ...

  [bangpypers@python.org]
  key1 = value1
  ...

The `main` section has the `username` and `password` for the Gmail account.
It also contains the email and name from whom the mail is sending.

The `to_addresses` section lists all the recipients email address and name.
There should be separate sections for each address to include user specific
values in the mail.  The values given in the email sections can be used in
template file using the Jinja2 macro syntax.  In the above example,
the `value` corresponding to `key1` can be used in the mail like this:
`{{ key1 }}``.

The template file use the Jina2 template language.

