def my_signal(app, template_rendered, message_flashed):
    @template_rendered.connect_via(app)
    def when_template_rendered(sender, template, context, **extra):
        print('Hi, Zahar! Template %s is rendered with %s' % (str(template.name), str(context)))

    def log_template_renders(sender, template, context, **extra):
        sender.logger.debug('Hello, admin! Rendering template "%s" with context %s',
                            template.name or 'string template',
                            context)

    template_rendered.connect(log_template_renders, app)

    recorded = []

    def record(message, category, **extra):
        recorded.append((str(message), category))
        print(recorded)

    message_flashed.connect(record, app)

    def log_template_renders(sender, template, context, **extra):
        sender.logger.debug('Rendering template "%s" with context %s',
                            template.name or 'string template',
                            context)

    template_rendered.connect(log_template_renders, app)