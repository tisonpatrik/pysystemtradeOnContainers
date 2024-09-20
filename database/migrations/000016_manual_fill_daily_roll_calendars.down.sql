-- Down migration (undoing any changes is unnecessary for manual refresh)
DO $$
BEGIN
    -- Typically no "down" operation is needed for manual refreshes
    RAISE NOTICE 'No down operation needed for refreshing continuous aggregates';
END $$;
