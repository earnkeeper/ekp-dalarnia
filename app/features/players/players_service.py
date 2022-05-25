class PlayersService:
    async def get_documents(self, form_values):
        documents = []

        for form_value in form_values:
            documents.append(
                {
                    "id": form_value["address"]
                }
            )

        return documents
