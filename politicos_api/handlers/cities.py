# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
#  for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

from politicos_api.cache import cache
from politicos_api.handlers.base import BaseHandler


class CitiesHandler(BaseHandler):

    @cache(5)
    async def get(self):
        body = {
            'from': self.per_page * (self.page - 1),
        }

        result = await self.es.search(
            index='cities',
            body=body,
            size=self.per_page,
        )

        response = {
            'meta': self.get_meta(result),
            'objects': [
                x.get('_source')
                for x in result.get('hits', {}).get('hits', {})
            ]
        }

        await self.json_response(response)


class CitiesSuggestHandler(BaseHandler):

    @cache(5)
    async def get(self):
        await self.suggest_response(
            'nm_ue',
            ['sg_ue'],
        )
