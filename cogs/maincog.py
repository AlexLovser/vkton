from vkton.classes import Commands, Context


@Commands.command(keywords=['начать'], back_to='start')
def start(ctx: Context):
    # print('+', self, '+',  ctx)
    ctx.user.send(
        'COG WORK!!!'
    )


