from typing import Union
import disnake
import asyncio
from disnake.ext import commands, tasks
from roucore.bot import RoucBot
class Profile(commands.Cog):
    def __init__(self, bot: RoucBot):
        self.bot: RoucBot = bot

    async def on_cog_load(self):
        self.bot.logger.debug('Cog "Profile" loaded')

    @commands.command(
        name = 'avatar',
        aliases = ['аватар'],
        brief = 'bot.commands.avatar.brief',
        description = 'bot.commands.avatar.description'
    )
    async def __avatar(self, ctx: commands.Context, member = None):
        try: 
            member = await commands.converter.MemberConverter().convert(ctx, member) if member is not None else ctx.author
            title = self.bot.translate('bot.commands.avatar.body.author_avatar') if ctx.author == member else self.bot.translate('bot.commands.avatar.body.member_avatar')
            avemb = disnake.Embed(
                title=title.format(str(member)),
                colour=self.bot.defaultcolor
            ).set_image(url=member.avatar.url if member is not None else ctx.author.avatar.url)
            await ctx.send(embed=avemb)
        except commands.errors.MemberNotFound:
            await ctx.send(embed=self.bot.errembed(self.bot.translate('bot.errors.unknown_user').format(member, "")))

    @commands.command(
        name = 'user',
        aliases = ['юзер', 'пользователь', 'aboutuser', 'userinfo', 'опользователе', 'profile', 'профиль'],
        brief = 'bot.commands.user.brief',
        description = 'bot.commands.user.description'
    )
    async def __user(self, ctx: commands.Context, user: str = None):
        translate = lambda s: self.bot.translate(s, 'en') # alias
        try:
            user = await commands.converter.MemberConverter().convert(ctx, user) if user is not None else ctx.author
        except commands.errors.MemberNotFound:
            try:
                user = await commands.converter.UserConverter().convert(ctx, user)
            except commands.errors.UserNotFound:
                return await ctx.send(embed=self.bot.errembed(translate('bot.errors.unknown_user').format(user, "")))
        user: disnake.Member
        useremb = disnake.Embed(
            colour = user.accent_color if user.accent_color is not None else self.bot.defaultcolor,
            title = translate('bot.commands.user.body.title').format(user.name),
            #description = '' # here will be bio
        )
        useremb.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        useremb.set_image(user.banner.url) if user.banner else None

        # okay let's go
        # identifcation info
        useremb.add_field(
            name = translate('bot.commands.user.body.username').format(user),
            value = translate('bot.commands.user.body.userid').format(user.id),
            inline = False
        )
        # when user joined to discord (and server if it is member)
        useremb.add_field(
            name = '** **', # trick to make it empty
            value = f'{translate("bot.commands.user.body.joineddiscord")}: {disnake.utils.format_dt(user.created_at, "R")}'\
                +(f'\n{translate("bot.commands.user.body.joinedserver")}: {disnake.utils.format_dt(user.joined_at, "R")}' if isinstance(user, disnake.Member) else '')
        )
        # standard status
        if user.status == disnake.Status.online:
            curstdstatus = f'<:online:989860351791218688>{translate("bot.commands.user.body.standardstatus.enum.online")}'
        if user.status == disnake.Status.idle:
            curstdstatus = f'<:idle:989860315195904020>{translate("bot.commands.user.body.standardstatus.enum.idle")}'
        if user.status == disnake.Status.dnd:
            curstdstatus = f'<:dnd:989860296090869810>{translate("bot.commands.user.body.standardstatus.enum.dnd")}'
        if user.status == disnake.Status.offline:
            curstdstatus = f'<:offline:989860347072639066>{translate("bot.commands.user.body.standardstatus.enum.offline")}'
        if user.status == disnake.Status.streaming:
            curstdstatus = f'<:streaming:989860377875578950>{translate("bot.commands.user.body.standardstatus.enum.streaming")}'
        useremb.add_field(
            name = '** **',
            value = f'{translate("bot.commands.user.body.standardstatus.pre")}: {curstdstatus}',
            inline = False
        )
        await ctx.send(embed = useremb)


def setup(bot):
    bot.add_cog(Profile(bot))
    bot.logger.debug('Cog "Profile" was added')
def teardown(bot):
    bot.logger.debug('Cog "Profile" was removed')