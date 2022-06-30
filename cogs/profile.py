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
        aliases = ['аватар'],
        brief = 'bot.commands.avatar.brief',
        description = 'bot.commands.avatar.description'
    )
    async def avatar(self, ctx: commands.Context, member = None):
        lang = (await self.bot.db.fetchrow(f"""SELECT locale FROM guilds WHERE id = {ctx.guild.id}"""))['locale']
        try: 
            member = await commands.converter.MemberConverter().convert(ctx, member) if member is not None else ctx.author
            title = self.bot.translate('bot.commands.avatar.body.author_avatar', lang) if ctx.author == member else self.bot.translate('bot.commands.avatar.body.member_avatar', lang)
            await ctx.send(embed=disnake.Embed(
                    title=title.format(member),
                    colour=self.bot.defaultcolor
                ).set_image(url=member.avatar.url if member is not None else ctx.author.avatar.url)
            )
        except commands.errors.MemberNotFound:
            await ctx.send(embed=self.bot.errembed(self.bot.translate('bot.errors.unknown_user', lang).format(member, "")))

    @commands.command(
        aliases = ['юзер', 'пользователь', 'aboutuser', 'userinfo', 'опользователе', 'profile', 'профиль'],
        brief = 'bot.commands.user.brief',
        description = 'bot.commands.user.description'
    )
    async def user(self, ctx: commands.Context, user: str = None):
        lang = (await self.bot.db.fetchrow(f"""SELECT locale FROM guilds WHERE id = {ctx.guild.id}"""))['locale']
        translate = lambda s: self.bot.translate("bot.commands.user."+s, lang) # alias
        try:
            user = await commands.converter.MemberConverter().convert(ctx, user) if user is not None else ctx.author
        except commands.errors.MemberNotFound:
            try:
                user = await commands.converter.UserConverter().convert(ctx, user)
            except commands.errors.UserNotFound:
                return await ctx.send(embed=self.bot.errembed(self.bot.translate('bot.errors.unknown_user').format(user, "")))
        useremb = disnake.Embed(
            colour = user.accent_color if user.accent_color is not None else user.color if user.color is not None else self.bot.defaultcolor,
            title = translate('body.title').format(user.name),
            #description = '' # here will be bio
        )
        useremb.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        useremb.set_image(user.banner.url) if user.banner else None

        # okay let's go
        # identifcation info
        useremb.add_field(
            name = translate('body.username').format(user),
            value = translate('body.userid').format(user.id),
            inline = False
        )
        # when user joined to discord (and server if it is member)
        useremb.add_field(
            name = '** **', # trick to make it empty
            value = f'{translate("body.joineddiscord")}: {disnake.utils.format_dt(user.created_at, "R")}'+
                (f'\n{translate("body.joinedserver")}: {disnake.utils.format_dt(user.joined_at, "R")}' if isinstance(user, disnake.Member) else '')
        )
        if getattr(user, "status", False):
            # standard status
            if user.status == disnake.Status.online:
                curstdstatus = f'<:online:989860351791218688>{translate("body.standardstatus.enum.online")}'
            if user.status == disnake.Status.idle:
                curstdstatus = f'<:idle:989860315195904020>{translate("body.standardstatus.enum.idle")}'
            if user.status == disnake.Status.dnd:
                curstdstatus = f'<:dnd:989860296090869810>{translate("body.standardstatus.enum.dnd")}'
            if user.status == disnake.Status.offline:
                curstdstatus = f'<:offline:989860347072639066>{translate("body.standardstatus.enum.offline")}'
            if user.status == disnake.Status.streaming:
                curstdstatus = f'<:streaming:989860377875578950>{translate("body.standardstatus.enum.streaming")}'

            useremb.add_field(
                name = '** **',
                value = f'{translate("body.standardstatus.pre")}: {curstdstatus}',
                inline = False
            )
        # user activity (for example "Playing `game name`")
        if getattr(user, 'activity', None) is not None:
            act = translate("body.activity."+('spotify' if getattr(user.activity, "track_id", None) is not None else str(user.activity.type).replace("ActivityType.", "")))
            if user.activity.type == disnake.ActivityType.streaming:
                activity = act.format(f'{user.activity.name} ({user.activity.twitch_name})')
            elif user.activity.type == disnake.ActivityType.listening:
                activity = act.format(user.activity.title or user.activity.name)
            # elif user.activity.type == disnake.ActivityType.custom:
            #     pass
            elif user.activity.type in (disnake.ActivityType.watching, disnake.ActivityType.competing, disnake.ActivityType.playing, disnake.ActivityType.custom):
                activity = act.format(user.activity.name)
            useremb.add_field(
                name = translate("body.activity.title"),
                value=activity,
                inline = False
            )
        # data from bot (level and another things)
        #useremb.add_field(name="", value="")

        await ctx.send(embed = useremb)


def setup(bot):
    bot.add_cog(Profile(bot))
    bot.logger.debug('Cog "Profile" was added')
def teardown(bot):
    bot.logger.debug('Cog "Profile" was removed')