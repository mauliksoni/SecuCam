package com.usa.secucam.secucam;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

/**
 * Adapter to bind a ToDoItem List to a view
 */
public class ToDoItemAdapter extends ArrayAdapter<ToDoItem> {

	/**
	 * Adapter context
	 */
	Context mContext;

	/**
	 * Adapter View layout
	 */
	int mLayoutResourceId;

	public ToDoItemAdapter(Context context, int layoutResourceId) {
		super(context, layoutResourceId);

		mContext = context;
		mLayoutResourceId = layoutResourceId;
	}

	/**
	 * Returns the view for a specific item on the list
	 */
	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		View row = convertView;

		final ToDoItem currentItem = getItem(position);

		if (row == null) {
			LayoutInflater inflater = ((Activity) mContext).getLayoutInflater();
			row = inflater.inflate(mLayoutResourceId, parent, false);
		}

		row.setTag(currentItem);
		final CheckBox checkBox = (CheckBox) row.findViewById(R.id.checkToDoItem);

        final Button button= (Button)row.findViewById(R.id.btnwatch);
        button.setEnabled(true);
        button.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                    if (mContext instanceof MainActivity) {
                        MainActivity activity = (MainActivity) mContext;
                        activity.watch(currentItem);
                    }
            }
        });

        DateFormat utcdf = new SimpleDateFormat("yy-MM-dd'T'HH:mm:ss.SSS");
        DateFormat dallasdf=new SimpleDateFormat("yy-MM-dd HH:mm");

        TimeZone utctz=TimeZone.getTimeZone("UTC");
        TimeZone dallastz = TimeZone.getTimeZone("America/Chicago");

        String dallasDate="";

        utcdf.setTimeZone(utctz);
        dallasdf.setTimeZone(dallastz);

        try {
            Date myDate = utcdf.parse(currentItem.GetTs());
            dallasDate = dallasdf.format(myDate).toString();
        } catch (ParseException e) {
            e.printStackTrace();
        }


        checkBox.setText(dallasDate);
		checkBox.setChecked(false);
		checkBox.setEnabled(true);

		checkBox.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View arg0) {
				if (checkBox.isChecked()) {
					checkBox.setEnabled(false);
					if (mContext instanceof MainActivity) {
						MainActivity activity = (MainActivity) mContext;
						activity.checkItem(currentItem);
					}
				}
			}
		});

		return row;
	}

}
