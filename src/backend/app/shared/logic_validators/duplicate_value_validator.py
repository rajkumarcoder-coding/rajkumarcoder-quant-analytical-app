class CommaSeparatedDeduplicator:
    @staticmethod
    def dedupe(
            value: str,
            *,
            normalize: bool = True,
            keep_order: bool = True,
    ) -> str:
        """
        Remove duplicate values from a comma-separated string.

        Args:
            value: Comma-separated string (e.g. "AAPL,MSFT,AAPL")
            normalize: Strip spaces and uppercase values
            keep_order: Preserve first-seen order

        Returns:
            Deduplicated comma-separated string
        """
        if not value:
            return ""

        items = [v.strip() for v in value.split(",") if v.strip()]

        if normalize:
            items = [v.upper() for v in items]

        if keep_order:
            seen = set()
            unique_items = []
            for item in items:
                if item not in seen:
                    seen.add(item)
                    unique_items.append(item)
        else:
            unique_items = sorted(set(items))

        return ",".join(unique_items)
